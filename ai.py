import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def explain_recommendation(profile, recommendations):

    recommendations_text = "\n".join(
        f"{i + 1}. {item['name']} — {item['score']}%"
        for i, item in enumerate(recommendations)
    )

    prompt = f"""
Ты — AI-консультант по выбору детско-юношеского спорта.

Твоя задача — помочь родителю понять результаты
анкетирования ребёнка.

ВАЖНЫЕ ПРАВИЛА:

1. Не ставь медицинских диагнозов.
2. Не утверждай, что конкретный спорт медицински показан.
3. Напоминай, что окончательный выбор желательно обсудить
   с тренером и при необходимости врачом.
4. Не пугай родителя.
5. Отвечай простым русским языком.
6. Не придумывай факты о ребёнке.
7. Не меняй рейтинг самостоятельно.

ПРОФИЛЬ:

Возраст: {profile['age']}

Физические качества:
{profile['qualities']}

Предпочтения:
{profile['preferences']}

РЕЗУЛЬТАТ АЛГОРИТМА:

{recommendations_text}

Сформируй ответ:

🏆 ТОП-5 видов спорта

Для каждого из первых трёх:
- название;
- почему подходит;
- какие качества поможет развивать.

В конце напиши:
"Рекомендация носит информационный характер. Перед началом
занятий стоит посетить пробную тренировку и обсудить выбор
с квалифицированным тренером."
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text