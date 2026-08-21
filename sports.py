# -*- coding: utf-8 -*-

SPORTS = {
    "Спортивная акробатика": {
        "emoji": "🤸",
        "min_age": 5,
        "max_age": 18,
    },

    "Прыжки на батуте": {
        "emoji": "🤸",
        "min_age": 5,
        "max_age": 18,
    },

    "Бокс": {
        "emoji": "🥊",
        "min_age": 8,
        "max_age": 18,
    },

    "Дзюдо": {
        "emoji": "🥋",
        "min_age": 6,
        "max_age": 18,
    },

    "Самбо": {
        "emoji": "🥋",
        "min_age": 7,
        "max_age": 18,
    },

    "Вольная борьба": {
        "emoji": "🤼",
        "min_age": 7,
        "max_age": 18,
    },

    "Стрельба из лука": {
        "emoji": "🏹",
        "min_age": 8,
        "max_age": 18,
    },

    "Тяжёлая атлетика": {
        "emoji": "🏋️",
        "min_age": 10,
        "max_age": 18,
    },

    "ММА": {
        "emoji": "🥊",
        "min_age": 10,
        "max_age": 18,
    },
}


def get_available_sports(age):
    """
    Возвращает виды спорта, допустимые для указанного возраста
    согласно возрастным ограничениям, заданным для проекта.
    """

    result = []

    for sport, data in SPORTS.items():
        if data["min_age"] <= age <= data["max_age"]:
            result.append(sport)

    return result