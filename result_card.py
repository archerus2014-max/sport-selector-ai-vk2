# -*- coding: utf-8 -*-

"""
SPORT SELECTOR AI V8.3

Красивое оформление результата VK
"""


def progress_bar(percent):

    total = 10

    filled = int(percent / 10)

    if filled > total:
        filled = total

    if filled < 0:
        filled = 0


    return (
        "█" * filled +
        "░" * (total - filled)
    )



def create_result_card(results, answers, explanation):

    if not results:

        return (
            "❌ Не удалось определить "
            "спортивное направление."
        )


    age = int(
        answers.get(
            "age",
            0
        )
    )


    height = answers.get(
        "height",
        "-"
    )


    weight = answers.get(
        "weight",
        "-"
    )


    best = results[0]


    text = []


    text.append(
        "🏆 SPORT SELECTOR AI"
    )

    text.append(
        "━━━━━━━━━━━━━━"
    )


    text.append(
        "🥇 ЛУЧШЕЕ НАПРАВЛЕНИЕ"
    )


    text.append(
        f"⭐ {best['sport']}"
    )


    text.append("")


    text.append(
        f"📊 Совместимость: {best['percent']}%"
    )


    text.append(
        progress_bar(
            best["percent"]
        )
    )


    text.append("")


    # ТОП-3

    text.append(
        "🏅 ТОП-3 ВИДА СПОРТА"
    )


    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]


    for index, item in enumerate(results[:3]):

        text.append(
            f"{medals[index]} "
            f"{item['sport']} — "
            f"{item['percent']}%"
        )


    text.append("")


    text.append(
        "🔎 ПОЧЕМУ ЭТО ПОДХОДИТ:"
    )


    for reason in explanation.get(
        "reasons",
        []
    ):

        text.append(
            f"✅ {reason}"
        )


    text.append("")


    text.append(
        "📈 ЧТО РАЗВИВАТЬ:"
    )


    for item in explanation.get(
        "improve",
        []
    ):

        text.append(
            f"🔹 {item}"
        )


    text.append("")


    text.append(
        "👤 ПАРАМЕТРЫ РЕБЁНКА:"
    )


    text.append(
        f"Возраст: {age} лет"
    )


    text.append(
        f"Рост: {height} см"
    )


    text.append(
        f"Вес: {weight} кг"
    )


    # отдельная логика 5-6 лет

    if age <= 6:

        text.append("")

        text.append(
            "👶 ВОЗРАСТНОЙ РЕЖИМ:"
        )

        text.append(
            "Для детей 5–6 лет "
            "оценивается общее физическое развитие."
        )

        text.append(
            "Главные задачи:"
        )

        text.append(
            "• координация"
        )

        text.append(
            "• гибкость"
        )

        text