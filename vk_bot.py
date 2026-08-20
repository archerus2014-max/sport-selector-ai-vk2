import os

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from engine import recommend
from ai import explain_recommendation


load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")


if not VK_TOKEN:
    print("ОШИБКА: VK_TOKEN не найден в .env")
    raise SystemExit


vk_session = vk_api.VkApi(token=VK_TOKEN)

vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)


# Здесь храним состояние пользователей.
users = {}


QUESTIONS = [
    {
        "key": "age",
        "text": "👶 Сколько лет ребёнку?\n\nНапишите число от 5 до 18."
    },

    {
        "key": "activity",
        "text": (
            "⚡ Насколько ребёнок активный?\n\n"
            "1 — очень спокойный\n"
            "2 — скорее спокойный\n"
            "3 — средне активный\n"
            "4 — активный\n"
            "5 — очень активный"
        )
    },

    {
        "key": "speed",
        "text": (
            "🏃 Как вы оцениваете скорость ребёнка?\n\n"
            "1 — низкая\n"
            "2 — ниже средней\n"
            "3 — средняя\n"
            "4 — высокая\n"
            "5 — очень высокая"
        )
    },

    {
        "key": "strength",
        "text": (
            "💪 Как вы оцениваете силу ребёнка?\n\n"
            "1 — низкая\n"
            "2 — ниже средней\n"
            "3 — средняя\n"
            "4 — высокая\n"
            "5 — очень высокая"
        )
    },

    {
        "key": "coordination",
        "text": (
            "🤸 Как у ребёнка с координацией движений?\n\n"
            "1 — сложно\n"
            "2 — ниже средней\n"
            "3 — средняя\n"
            "4 — хорошая\n"
            "5 — отличная"
        )
    },

    {
        "key": "endurance",
        "text": (
            "🏃‍♂️ Как с выносливостью?\n\n"
            "1 — быстро устаёт\n"
            "2 — ниже средней\n"
            "3 — средняя\n"
            "4 — хорошая\n"
            "5 — отличная"
        )
    },

    {
        "key": "flexibility",
        "text": (
            "🤸 Насколько ребёнок гибкий?\n\n"
            "1 — мало\n"
            "2 — ниже средней\n"
            "3 — средняя\n"
            "4 — гибкий\n"
            "5 — очень гибкий"
        )
    },

    {
        "key": "competition",
        "text": (
            "🏆 Как ребёнок относится к соревнованиям?\n\n"
            "1 — не любит\n"
            "2 — скорее не любит\n"
            "3 — нейтрально\n"
            "4 — любит\n"
            "5 — очень любит"
        )
    },

    {
        "key": "contact",
        "text": (
            "🥊 Как ребёнок относится к физическому контакту "
            "с соперником?\n\n"
            "1 — категорически не любит\n"
            "2 — скорее не любит\n"
            "3 — нейтрально\n"
            "4 — нормально относится\n"
            "5 — нравится"
        )
    },

    {
        "key": "individual",
        "text": (
            "🎯 Что больше подходит ребёнку?\n\n"
            "1 — предпочитает команду\n"
            "2 — скорее команду\n"
            "3 — без разницы\n"
            "4 — скорее индивидуально\n"
            "5 — индивидуальные занятия"
        )
    },

    {
        "key": "team",
        "text": (
            "🤝 Насколько ребёнку нравится командная работа?\n\n"
            "1 — совсем не нравится\n"
            "2 — скорее не нравится\n"
            "3 — без разницы\n"
            "4 — нравится\n"
            "5 — очень нравится"
        )
    }
]


def send_message(user_id, message):

    vk.messages.send(
        user_id=user_id,
        random_id=0,
        message=message
    )


def start_test(user_id):

    users[user_id] = {
        "question": 0,
        "answers": {}
    }

    send_message(
        user_id,
        "👋 Здравствуйте!\n\n"
        "Я помогу подобрать ребёнку подходящие виды спорта.\n\n"
        "Это не медицинская диагностика, а "
        "информационная рекомендация.\n\n"
        "Начинаем! 🏆"
    )

    send_question(user_id)


def send_question(user_id):

    state = users[user_id]

    question_index = state["question"]

    if question_index >= len(QUESTIONS):

        finish_test(user_id)

        return

    question = QUESTIONS[question_index]

    send_message(
        user_id,
        f"Вопрос {question_index + 1} из {len(QUESTIONS)}\n\n"
        + question["text"]
    )


def finish_test(user_id):

    state = users[user_id]

    answers = state["answers"]

    profile = {
        "age": answers["age"],

        "qualities": {
            "speed": answers["speed"],
            "strength": answers["strength"],
            "coordination": answers["coordination"],
            "endurance": answers["endurance"],
            "flexibility": answers["flexibility"],
        },

        "preferences": {
            "competition": answers["competition"],
            "contact": answers["contact"],
            "individual": answers["individual"],
            "team": answers["team"],
        }
    }

    recommendations = recommend(profile)

    send_message(
        user_id,
        "⏳ Анализирую ответы и подбираю виды спорта..."
    )

    explanation = explain_recommendation(
        profile,
        recommendations
    )

    send_message(
        user_id,
        explanation
    )

    send_message(
        user_id,
        "Если хотите пройти тест заново, "
        "напишите: СПОРТ"
    )

    del users[user_id]


def process_answer(user_id, text):

    state = users[user_id]

    question_index = state["question"]

    question = QUESTIONS[question_index]

    key = question["key"]

    try:

        value = int(text)

    except ValueError:

        send_message(
            user_id,
            "Пожалуйста, введите число от 1 до 5."
        )

        return

    if key == "age":

        if value < 5 or value > 18:

            send_message(
                user_id,
                "Пожалуйста, укажите возраст "
                "от 5 до 18 лет."
            )

            return

    else:

        if value < 1 or value > 5:

            send_message(
                user_id,
                "Пожалуйста, введите число от 1 до 5."
            )

            return

    state["answers"][key] = value

    state["question"] += 1

    send_question(user_id)


print("=" * 60)
print("AI SPORT CONSULTANT")
print("VK BOT")
print("=" * 60)

print("VK подключен.")
print("Бот запущен.")
print("Ожидаю сообщения...")
print()


for event in longpoll.listen():

    if event.type != VkEventType.MESSAGE_NEW:
        continue

    if not event.to_me:
        continue

    user_id = event.user_id

    text = event.text.strip()

    print(
        f"[VK] {user_id}: {text}"
    )

    if text.lower() in [
        "спорт",
        "старт",
        "start",
        "начать"
    ]:

        start_test(user_id)

        continue

    if user_id in users:

        process_answer(
            user_id,
            text
        )

        continue

    send_message(
        user_id,
        "👋 Привет!\n\n"
        "Я AI-консультант по выбору "
        "детского спорта.\n\n"
        "Чтобы начать тест, напишите:\n"
        "🏆 СПОРТ"
    )