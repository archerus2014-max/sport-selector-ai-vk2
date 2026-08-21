# -*- coding: utf-8 -*-

"""
engine.py V10.1

СПОРТИВНЫЙ АГЕНТ
Подбор спортивного направления для ребенка
"""


from sport_standards import (
    SPORT_STANDARDS,
    get_allowed_sports,
    get_not_allowed_sports
)



# =====================================================
# Расчет ИМТ
# =====================================================

def calculate_bmi(height, weight):

    try:

        h = int(height) / 100
        w = int(weight)

        if h <= 0:
            return 0

        return round(
            w / (h * h),
            1
        )

    except:

        return 0



# =====================================================
# Главный спортивный агент
# =====================================================

def recommend(data):


    age = int(
        data.get(
            "age",
            0
        )
    )


    height = data.get(
        "height",
        "-"
    )


    weight = data.get(
        "weight",
        "-"
    )


    bmi = calculate_bmi(
        height,
        weight
    )



    allowed = get_allowed_sports(
        age
    )


    not_allowed = get_not_allowed_sports(
        age
    )



    scores = {}



    for sport in allowed:

        scores[sport] = 0



    # =========================================
    # Получаем характеристики ребенка
    # =========================================


    strength = data.get(
        "strength",
        ""
    )


    speed = data.get(
        "speed",
        ""
    )


    coordination = data.get(
        "coordination",
        ""
    )


    endurance = data.get(
        "endurance",
        ""
    )


    flexibility = data.get(
        "flexibility",
        ""
    )


    competition = data.get(
        "competition",
        ""
    )


    contact = data.get(
        "contact",
        ""
    )



    # =========================================
    # Оценка спорта
    # =========================================


    for sport in scores:


        category = SPORT_STANDARDS[sport]["category"]



        if category == "единоборство":


            if "Сильный" in strength:
                scores[sport] += 15


            if "быстрый" in speed.lower():
                scores[sport] += 10


            if "борьбу" in contact:
                scores[sport] += 15


            if "выносливый" in endurance.lower():
                scores[sport] += 10



        if category == "координация":


            if "Хорошо" in coordination:
                scores[sport] += 15


            if "гибкий" in flexibility.lower():
                scores[sport] += 15


            if "быстрый" in speed.lower():
                scores[sport] += 10



        if category == "точность":


            if "Хорошо" in coordination:
                scores[sport] += 15



        if category == "силовой спорт":


            if "Сильный" in strength:
                scores[sport] += 20



    # =========================================
    # Телосложение
    # =========================================


    if bmi:


        if bmi < 18:


            for s in [
                "Спортивная акробатика",
                "Прыжки на батуте"
            ]:

                if s in scores:
                    scores[s] += 10



        elif bmi > 23:


            for s in [
                "Бокс",
                "Самбо",
                "Вольная борьба"
            ]:

                if s in scores:
                    scores[s] += 10



    ranking = sorted(

        scores.items(),

        key=lambda x:x[1],

        reverse=True

    )



    # =========================================
    # Формирование ответа
    # =========================================


    text = f"""

🏆 СПОРТИВНЫЙ АГЕНТ


Анализ ребенка:

Возраст: {age} лет
Рост: {height} см
Вес: {weight} кг
Индекс массы тела: {bmi}


"""



    # =========================================
    # Дети младшего возраста
    # =========================================


    if age < 6:


        text += """

👶 Возрастная группа:
раннее физическое развитие


На данном этапе рекомендуется
не спортивная специализация,
а развитие физических качеств.


✅ Рекомендуемые направления:


🤸 Спортивно-оздоровительная группа
по спортивной акробатике


🤸 Спортивно-оздоровительная группа
по прыжкам на батуте


Также рекомендуется:

• общая физическая подготовка;
• развитие координации;
• развитие гибкости;
• формирование правильной осанки.


"""


        text += """

🚀 Перспективные направления после
достижения возраста спортивной подготовки:


"""


        for item in not_allowed[:5]:

            text += (
                f"• {item['sport']} — "
                f"после {item['age']} лет\n"
            )



    else:


        if ranking:


            text += """

✅ Наиболее подходящие направления:


"""


            place = 1


            for sport, score in ranking[:5]:


                percent = min(
                    95,
                    60 + score
                )


                text += (
                    f"{place}. {sport} — {percent}%\n"
                )


                place += 1



    # =========================================
    # Информация о возрасте
    # =========================================


    if not_allowed and age >= 6:


        text += """



📚 Направления, где требуется
достижение возраста спортивной подготовки:


"""


        for item in not_allowed[:5]:

            text += (
                f"• {item['sport']} "
                f"(с {item['age']} лет)\n"
            )



    text += """



📌 Рекомендация спортивного агента:


Рекомендуется посетить пробное занятие.
Окончательное решение принимается тренером
после оценки двигательных способностей ребенка.


"""



    return text