# -*- coding: utf-8 -*-

SPORTS = {

    "Спортивная акробатика": {
        "emoji": "🤸",
        "min_age": 5,
        "max_age": 18,
        "qualities": [
            "координация",
            "гибкость",
            "скорость"
        ]
    },


    "Прыжки на батуте": {
        "emoji": "🤸",
        "min_age": 5,
        "max_age": 18,
        "qualities": [
            "координация",
            "скорость",
            "гибкость"
        ]
    },


    "Бокс": {
        "emoji": "🥊",
        "min_age": 8,
        "max_age": 18,
        "qualities": [
            "сила",
            "скорость",
            "контакт"
        ]
    },


    "Дзюдо": {
        "emoji": "🥋",
        "min_age": 6,
        "max_age": 18,
        "qualities": [
            "координация",
            "сила",
            "контакт"
        ]
    },


    "Самбо": {
        "emoji": "🥋",
        "min_age": 7,
        "max_age": 18,
        "qualities": [
            "сила",
            "контакт",
            "выносливость"
        ]
    },


    "Вольная борьба": {
        "emoji": "🤼",
        "min_age": 7,
        "max_age": 18,
        "qualities": [
            "сила",
            "выносливость",
            "контакт"
        ]
    },


    "Стрельба из лука": {
        "emoji": "🏹",
        "min_age": 8,
        "max_age": 18,
        "qualities": [
            "координация",
            "концентрация"
        ]
    },


    "Тяжелая атлетика": {
        "emoji": "🏋️",
        "min_age": 10,
        "max_age": 18,
        "qualities": [
            "сила"
        ]
    },


    "ММА": {
        "emoji": "🥊",
        "min_age": 10,
        "max_age": 18,
        "qualities": [
            "сила",
            "контакт",
            "выносливость"
        ]
    }

}



def get_available_sports(age):

    result = []


    for sport, data in SPORTS.items():

        if data["min_age"] <= age <= data["max_age"]:

            result.append(sport)


    return result