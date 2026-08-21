# -*- coding: utf-8 -*-
"""
VK BOT — SPORT SELECTOR AI V7
15 вопросов по шкале 1–5 + пол + рост + вес.
"""

import json
import os
import time
from pathlib import Path

import vk_api
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from engine import recommend, explain_recommendation

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN", "").strip()
VK_GROUP_ID = int(os.getenv("VK_GROUP_ID", "154840474").strip())

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

QUESTIONS = [
    ("age", "Сколько лет ребёнку?\nВведите целое число от 5 до 18."),
    ("sex", "Пол ребёнка?\n1 — мальчик\n2 — девочка"),
    ("height", "Какой рост ребёнка?\nВведите рост в сантиметрах. Например: 128"),
    ("weight", "Какой вес ребёнка?\nВведите вес в килограммах. Например: 27"),
    ("activity", "1/15. Насколько ребёнок активен в обычной жизни?\n1 — почти не двигается\n2 — мало активен\n3 — обычная активность\n4 — очень активный\n5 — постоянно в движении"),
    ("speed", "2/15. Как ребёнок проявляет себя в быстрых движениях и беге?\n1 — заметно медленный\n2 — скорее медленный\n3 — средний\n4 — быстрый\n5 — очень быстрый"),
    ("strength", "3/15. Как развита сила ребёнка относительно сверстников?\n1 — заметно слабее\n2 — скорее слабый\n3 — средний уровень\n4 — сильный\n5 — очень сильный"),
    ("endurance", "4/15. Как ребёнок переносит продолжительную физическую нагрузку?\n1 — быстро устаёт\n2 — устаёт быстрее большинства\n3 — обычная выносливость\n4 — хорошо переносит нагрузку\n5 — может долго заниматься без заметной усталости"),
    ("coordination", "5/15. Как ребёнок осваивает новые движения?\n1 — очень трудно\n2 — скорее трудно\n3 — нормально\n4 — быстро\n5 — очень быстро и точно"),
    ("flexibility", "6/15. Насколько ребёнок гибкий?\n1 — очень негибкий\n2 — гибкость ниже средней\n3 — средняя\n4 — хорошая\n5 — очень хорошая"),
    ("reaction", "7/15. Какова реакция ребёнка на быстро меняющуюся ситуацию?\n1 — медленная\n2 — скорее медленная\n3 — средняя\n4 — быстрая\n5 — очень быстрая"),
    ("balance", "8/15. Как ребёнок удерживает равновесие?\n1 — трудно\n2 — скорее трудно\n3 — нормально\n4 — хорошо\n5 — отлично"),
    ("rhythm", "9/15. Как ребёнок чувствует ритм и повторяет движения под музыку?\n1 — очень трудно\n2 — скорее трудно\n3 — нормально\n4 — хорошо\n5 — отлично"),
    ("team", "10/15. Что ребёнку ближе?\n1 — предпочитает заниматься одному\n2 — скорее индивидуально\n3 — без разницы\n4 — любит работать с другими\n5 — очень любит команду и группу"),
    ("contact", "11/15. Как ребёнок относится к физическому контакту и соперничеству?\n1 — категорически не любит\n2 — скорее не любит\n3 — спокойно относится\n4 — нормально воспринимает\n5 — любит контактное соперничество"),
    ("competition", "12/15. Как ребёнок относится к соревнованиям?\n1 — не любит\n2 — скорее не любит\n3 — безразлично\n4 — любит\n5 — очень любит соревноваться"),
    ("precision", "13/15. Насколько хорошо ребёнок выполняет точные действия?\n1 — очень трудно\n2 — скорее трудно\n3 — средне\n4 — хорошо\n5 — очень точно"),
    ("discipline", "14/15. Как ребёнок выполняет инструкции тренера или взрослого?\n1 — очень трудно\n2 — часто отвлекается\n3 — обычно выполняет\n4 — хорошо соблюдает\n5 — очень дисциплинирован"),
    ("interest", "15/15. Насколько ребёнку вообще интересны занятия спортом?\n1 — совсем не интересны\n2 — интерес небольшой\n3 — иногда интересно\n4 — нравится спорт\n5 — очень любит заниматься"),
]

def load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_users(users):
    USERS_FILE.write_text(
        json.dumps(users, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_user(users, peer_id):
    key = str(peer_id)
    if key not in users:
        users[key] = {
            "state": "idle",
            "answers": {},
            "question_index": 0,
        }
    return users[key]

def keyboard_start():
    kb = VkKeyboard(one_time=True)
    kb.add_button("СТАРТ", color=VkKeyboardColor.POSITIVE)
    return kb.get_keyboard()

def send(vk, peer_id, text, keyboard=None):
    kwargs = {
        "peer_id": peer_id,
        "message": text,
        "random_id": 0,
    }
    if keyboard:
        kwargs["keyboard"] = keyboard
    vk.messages.send(**kwargs)

def parse_number(text):
    try:
        return float(text.strip().replace(",", "."))
    except Exception:
        return None

def start_test(vk, peer_id, user, users):
    user["state"] = "question"
    user["answers"] = {}
    user["question_index"] = 0
    save_users(users)

    send(
        vk,
        peer_id,
        "🏁 ТЕСТ «ПОДБОР ВИДА СПОРТА»\n\n"
        "Сначала определим возраст, пол, рост и вес ребёнка, "
        "затем зададим 15 вопросов.\n\n"
        "Для последних 15 вопросов используется шкала 1–5. "
        "Это позволяет сделать оценку гибче.\n\n"
        + QUESTIONS[0][1]
    )

def finish_test(vk, peer_id, user, users):
    answers = user["answers"]
    age = int(answers["age"])

    results = recommend(answers)

    user["state"] = "finished"
    user["last_result"] = results
    save_users(users)

    sex_text = "мальчик" if int(answers["sex"]) == 1 else "девочка"
    height = answers["height"]
    weight = answers["weight"]

    lines = [
        "🏁 ТЕСТ ЗАВЕРШЁН!",
        "",
        f"Возраст: {age} лет",
        f"Пол: {sex_text}",
        f"Рост: {height:g} см",
        f"Вес: {weight:g} кг",
        "",
        "🏆 ВАШИ РЕКОМЕНДАЦИИ:",
    ]

    medals = ["🥇", "🥈", "🥉"]

    for i, item in enumerate(results[:3]):
        lines.append(
            f"{medals[i]} {item['sport']} — {item['percent']}%"
        )

    if results:
        best = results[0]
        explanation = explain_recommendation(best, answers)

        lines += [
            "",
            f"🔎 ПОЧЕМУ: {best['sport']}",
            "• " + "; ".join(explanation["reasons"]) + ".",
            "",
            "📈 ЧТО РАЗВИВАТЬ:",
            "• " + "; ".join(explanation["improve"]) + ".",
        ]

    if age <= 6:
        lines += [
            "",
            "👶 ВОЗРАСТНОЙ РЕЖИМ:",
            "Для детей 5–6 лет рекомендации трактуются "
            "как направления общего физического развития.",
            "В этом возрасте тест не предлагает единоборства, "
            "тяжёлую атлетику и другие специализированные виды.",
        ]
    else:
        lines += [
            "",
            "📌 В результатах учитываются возраст, ответы на 15 вопросов, "
            "а также рост и вес ребёнка.",
        ]

    lines += [
        "",
        "⚠️ Важно: результат не является медицинским диагнозом "
        "или профессиональным заключением. Антропометрия используется "
        "только как дополнительный фактор.",
        "",
        "Для детей 5–17 лет ВОЗ рекомендует в среднем не менее "
        "60 минут умеренной или высокой физической активности в день.",
        "",
        "🔄 Хотите пройти тест ещё раз? Напишите: СТАРТ",
    ]

    send(vk, peer_id, "\n".join(lines), keyboard_start())

def handle_message(vk, peer_id, text, users):
    user = get_user(users, peer_id)
    cmd = text.strip().lower()

    if cmd in {"старт", "start", "/start", "начать", "тест"}:
        start_test(vk, peer_id, user, users)
        return

    if cmd in {"спорт", "виды спорта", "помощь", "help"}:
        send(
            vk,
            peer_id,
            "🏆 SPORT SELECTOR AI\n\n"
            "Бот подбирает спортивное направление по возрасту, "
            "полу, росту, весу и 15 характеристикам.\n\n"
            "Напишите СТАРТ, чтобы пройти тест.",
            keyboard_start(),
        )
        return

    if user["state"] != "question":
        send(
            vk,
            peer_id,
            "Чтобы начать подбор вида спорта, напишите: СТАРТ",
            keyboard_start(),
        )
        return

    idx = user["question_index"]

    if idx >= len(QUESTIONS):
        finish_test(vk, peer_id, user, users)
        return

    key, question = QUESTIONS[idx]
    value = parse_number(text)

    if key == "age":
        if value is None or value != int(value) or not 5 <= value <= 18:
            send(vk, peer_id, "Введите целый возраст от 5 до 18. Например: 5")
            return
        user["answers"][key] = int(value)

    elif key == "sex":
        if value not in (1, 2):
            send(vk, peer_id, "Введите 1 — мальчик или 2 — девочка.")
            return
        user["answers"][key] = int(value)

    elif key == "height":
        if value is None or not 80 <= value <= 220:
            send(vk, peer_id, "Введите рост в сантиметрах. Например: 128")
            return
        user["answers"][key] = round(value, 1)

    elif key == "weight":
        if value is None or not 10 <= value <= 150:
            send(vk, peer_id, "Введите вес в килограммах. Например: 27")
            return
        user["answers"][key] = round(value, 1)

    else:
        if value is None or value != int(value) or int(value) not in range(1, 6):
            send(vk, peer_id, "Введите только число от 1 до 5.")
            return
        user["answers"][key] = int(value)

    idx += 1
    user["question_index"] = idx
    save_users(users)

    if idx < len(QUESTIONS):
        send(vk, peer_id, QUESTIONS[idx][1])
    else:
        finish_test(vk, peer_id, user, users)

def main():
    if not VK_TOKEN:
        raise RuntimeError("VK_TOKEN не задан в .env")

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()

    vk.groups.getById(group_id=VK_GROUP_ID)
    longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

    print("=" * 60)
    print("SPORT SELECTOR AI — VK BOT V7")
    print("=" * 60)
    print(f"VK_GROUP_ID: {VK_GROUP_ID}")
    print("✅ VK подключен")
    print("✅ Long Poll запущен")
    print("✅ Бот готов принимать сообщения")
    print("=" * 60)

    users = load_users()

    for event in longpoll.listen():
        try:
            if event.type != VkBotEventType.MESSAGE_NEW:
                continue

            obj = event.object
            message = obj.get("message", obj)

            peer_id = message.get("peer_id")
            text = message.get("text", "")

            if peer_id is None:
                continue

            print(f"📩 {peer_id}: {text}")

            handle_message(vk, peer_id, text, users)

        except Exception as e:
            print(f"❌ Ошибка обработки: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
