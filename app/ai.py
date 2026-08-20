import json
import httpx
from .config import settings
from .sports import SPORTS

SYSTEM = '''Ты — AI-консультант спортивной школы по первичному выбору вида спорта для ребёнка.
Отвечай по-русски, доброжелательно, коротко и понятно родителю.
Нельзя ставить диагнозы, определять медицинскую пригодность или обещать спортивный результат.
Нельзя говорить, что тест научно определяет идеальный спорт. Это рекомендационный алгоритм.
При медицинских ограничениях направляй к врачу и тренеру.
Основывай объяснение на переданных результатах scoring engine, а не придумывай новые результаты.
Не выдумывай расписание, тренеров, цены или наличие мест — если этих данных нет, так и скажи.
'''

async def ask(messages):
    if not settings.OPENAI_API_KEY:
        return None
    body={"model":settings.OPENAI_MODEL,"input":[{"role":"system","content":SYSTEM},*messages],"max_output_tokens":700}
    async with httpx.AsyncClient(timeout=45) as client:
        r=await client.post("https://api.openai.com/v1/responses",headers={"Authorization":f"Bearer {settings.OPENAI_API_KEY}","Content-Type":"application/json"},json=body)
        if r.status_code>=400:
            return None
        data=r.json()
        return data.get("output_text")

async def explain_result(age,profile,results):
    payload={"age":age,"profile":profile,"top5":[{"sport":SPORTS[k]["name"],"score":s} for k,s in results[:5]]}
    prompt="Сформируй персональное объяснение результата. Дай ТОП-3 с причинами, затем один практический совет про пробные тренировки. Данные scoring engine:\n"+json.dumps(payload,ensure_ascii=False)
    return await ask([{"role":"user","content":prompt}])

async def chat(user_text,session):
    context={"age":session.get("age"),"profile":session.get("profile"),"top5":[{"sport":SPORTS[k]["name"],"score":s} for k,s in (session.get("results") or [])[:5]]}
    prompt="Контекст ребёнка и результата:\n"+json.dumps(context,ensure_ascii=False)+"\n\nВопрос родителя:\n"+user_text
    return await ask([{"role":"user","content":prompt}])
