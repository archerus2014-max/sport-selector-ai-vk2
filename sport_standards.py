# -*- coding: utf-8 -*-

"""
sport_standards.py V10

Нормативная база спортивного агента
Минимальный возраст начала спортивной подготовки
"""

SPORT_STANDARDS = {


    "Спортивная акробатика": {

        "min_age": 6,

        "category": "координация",

        "description":
        "Развитие гибкости, координации, силы и акробатических навыков."

    },


    "Прыжки на батуте": {

        "min_age": 6,

        "category": "координация",

        "description":
        "Развитие пространственной ориентации, скорости реакции и координации."

    },


    "Бокс": {

        "min_age": 8,

        "category": "единоборство",

        "description":
        "Развитие скорости, реакции, силы и тактического мышления."

    },


    "Дзюдо": {

        "min_age": 7,

        "category": "единоборство",

        "description":
        "Развитие координации, силы, гибкости и борьбы."

    },


    "Самбо": {

        "min_age": 7,

        "category": "единоборство",

        "description":
        "Развитие силы, выносливости и навыков борьбы."

    },


    "Вольная борьба": {

        "min_age": 7,

        "category": "единоборство",

        "description":
        "Развитие силовых качеств, ловкости и выносливости."

    },


    "Стрельба из лука": {

        "min_age": 8,

        "category": "точность",

        "description":
        "Развитие концентрации, стабильности и координации."

    },


    "Тяжелая атлетика": {

        "min_age": 10,

        "category": "силовой спорт",

        "description":
        "Развитие максимальной силы и скоростно-силовых качеств."

    },


    "ММА": {

        "min_age": 10,

        "category": "единоборство",

        "description":
        "Комплексная подготовка в ударных и борцовских дисциплинах."

    }


}



def get_allowed_sports(age):

    """
    Возвращает только виды спорта,
    соответствующие возрасту
    """

    result = []


    for sport, data in SPORT_STANDARDS.items():

        if age >= data["min_age"]:

            result.append(sport)


    return result



def get_not_allowed_sports(age):

    """
    Возвращает виды спорта,
    которые пока рано начинать
    """

    result = []


    for sport, data in SPORT_STANDARDS.items():

        if age < data["min_age"]:

            result.append(
                {
                    "sport": sport,
                    "age": data["min_age"]
                }
            )


    return result