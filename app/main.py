import json
from fastapi import FastAPI,Request
from .config import settings
from .questions import QUESTIONS,SAFETY_QUESTION
from .state import create,get,reset
from .engine import build_profile,score_sports,explain
from .sports import SPORTS
from .keyboards import keyboard,start_keyboard,stop_keyboard,restart_keyboard
from .vk import send_message
from .ai import explain_result,chat

app=FastAPI(title="Спорт-Подбор AI — VK")

@app.get("/health")
async def health(): return {"status":"ok","openai_configured":bool(settings.OPENAI_API_KEY),"vk_configured":bool(settings.VK_TOKEN)}

def norm(s): return " ".join((s or "").strip().lower().split())

def payload_value(raw):
    try:
        if isinstance(raw,dict): return raw.get("value")
        if isinstance(raw,str): return json.loads(raw).get("value")
    except Exception: pass
    return None

async def start(peer):
    s=create(peer)
    await send_message(peer,"👋 Привет! Я AI-консультант по выбору спорта для ребёнка. Пройду короткую анкету, затем алгоритм подберёт направления, а AI объяснит результат. Это не медицинская диагностика.\n\nСколько лет ребёнку?",stop_keyboard())

async def ask_q(peer,s):
    q=QUESTIONS[s["index"]]
    await send_message(peer,q["text"],keyboard([(label,label) for label,_ in q["options"]]))

async def result(peer,s):
    if s["medical"] in ("yes","unknown"):
        await send_message(peer,"⚠️ Я не могу самостоятельно оценивать медицинскую пригодность. При наличии или неизвестности ограничений сначала обсудите допустимую нагрузку с врачом и тренером.",start_keyboard()); reset(peer); return
    s["profile"]=build_profile(s["vectors"])
    s["results"]=score_sports(s["profile"],s["age"])
    ai=await explain_result(s["age"],s["profile"],s["results"])
    if not ai:
        medals=["🥇","🥈","🥉","4️⃣","5️⃣"]
        parts=["🏆 РЕЗУЛЬТАТ ПОДБОРА\n"]
        for i,(k,score) in enumerate(s["results"][:5]):
            parts.append(f"{medals[i]} {SPORTS[k]['emoji']} {SPORTS[k]['name']} — {score}%\nСовпали: {', '.join(explain(k,s['profile']))}.\n")
        parts.append("💡 Совет: попробовать 2–3 лидирующих направления на вводной тренировке.")
        ai="\n".join(parts)
    await send_message(peer,ai,restart_keyboard())
    # Keep session after result so the user can ask natural-language follow-ups.
    s["index"]="done"

async def process(peer,text,payload=None):
    t=norm(text); s=get(peer); pv=payload_value(payload)
    command=pv or t
    if command in ("start","спорт","подобрать спорт","начать","start"):
        await start(peer); return
    if command in ("restart","заново","пройти заново"):
        await start(peer); return
    if command in ("stop","стоп","отмена"):
        reset(peer); await send_message(peer,"Анкета остановлена.",start_keyboard()); return
    if not s:
        await send_message(peer,"Напишите «спорт», чтобы начать.",start_keyboard()); return
    if s.get("medical_pending"):
        val=pv
        if val not in ("yes","no","unknown"):
            for label,v in SAFETY_QUESTION["options"]:
                if norm(label)==t: val=v
        if val in ("yes","no","unknown"):
            s["medical"]=val; s.pop("medical_pending",None); await result(peer,s)
        else:
            await send_message(peer,SAFETY_QUESTION["text"],keyboard(SAFETY_QUESTION["options"]))
        return
    if s.get("index")=="done":
        answer=await chat(text,s)
        if answer: await send_message(peer,answer)
        else: await send_message(peer,"AI-режим сейчас недоступен. Проверьте OPENAI_API_KEY на сервере.")
        return
    idx=s["index"]
    if idx==0:
        try:
            age=int(t)
            if age<4 or age>17: raise ValueError
            s["age"]=age; s["index"]=1; await ask_q(peer,s)
        except ValueError: await send_message(peer,"Введите возраст числом от 4 до 17, например 8.")
        return
    q=QUESTIONS[idx]; vector=None
    for label,v in q["options"]:
        if norm(label)==t: vector=v; break
    if vector is None:
        await send_message(peer,"Выберите вариант кнопкой ниже.",keyboard([(label,label) for label,_ in q["options"]])); return
    s["vectors"].append(vector); s["answers"][q["key"]]=t; s["index"]+=1
    if s["index"]<len(QUESTIONS): await ask_q(peer,s)
    else:
        s["medical_pending"]=True
        await send_message(peer,SAFETY_QUESTION["text"],keyboard(SAFETY_QUESTION["options"]))

@app.post("/vk/callback")
async def callback(request:Request):
    body=await request.json()
    if body.get("type")=="confirmation": return settings.VK_CONFIRMATION_CODE
    if settings.VK_SECRET and body.get("secret")!=settings.VK_SECRET: return "ok"
    if body.get("type")!="message_new": return "ok"
    obj=body.get("object",{}); peer=obj.get("peer_id"); text=obj.get("text",""); payload=obj.get("payload")
    if peer is not None: await process(peer,text,payload)
    return "ok"
