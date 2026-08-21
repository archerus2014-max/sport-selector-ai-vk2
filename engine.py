# -*- coding: utf-8 -*-

"""
Sport Selector AI VK
ENGINE V9 CLOUD

Алгоритм подбора спорта
"""


SPORTS = {

    "Спортивная акробатика": {
        "skills": {
            "coordination": 5,
            "flexibility": 5,
            "balance": 5,
            "activity": 4
        }
    },


    "Прыжки на батуте": {
        "skills": {
            "coordination": 5,
            "speed": 5,
            "balance": 5,
            "activity": 4
        }
    },


    "Дзюдо": {
        "skills": {
            "coordination": 5,
            "balance": 5,
            "discipline": 5,
            "competition": 4
        }
    },


    "Самбо": {
        "skills": {
            "strength": 5,
            "competition": 5,
            "contact": 5,
            "discipline": 4
        }
    },


    "Вольная борьба": {
        "skills": {
            "strength": 5,
            "endurance": 5,
            "contact": 5
        }
    },


    "Бокс": {
        "skills": {
            "speed": 5,
            "strength": 4,
            "reaction": 5,
            "discipline": 5
        }
    },


    "ММА": {
        "skills": {
            "strength": 5,
            "speed": 5,
            "contact": 5
        }
    },


    "Стрельба из лука": {
        "skills": {
            "discipline": 5,
            "focus": 5,
            "stability": 5
        }
    },


    "Тяжёлая атлетика": {
        "skills": {
            "strength": 5,
            "discipline": 5,
            "power": 5
        }
    }

}



def calculate_age_bonus(age, sport):

    age = int(age)


    if age <= 6:

        if sport in [
            "Спортивная акробатика",
            "Прыжки на батуте"
        ]:
            return 20

        return -20



    if age <=10:

        if sport in [
            "Дзюдо",
            "Самбо",
            "Акробатика",
            "Прыжки на батуте"
        ]:
            return 10



    return 0




def recommend(data):


    age = data.get(
        "age",
        7
    )


    answers = data.get(
        "answers",
        {}
    )



    result=[]



    for sport,info in SPORTS.items():


        score=0
        count=0


        for skill,value in info["skills"].items():


            child_value = int(
                answers.get(
                    skill,
                    3
                )
            )


            score += (
                10 -
                abs(
                    value-child_value
                )
            )


            count+=1



        percent = (
            score / count
        ) * 10



        percent += calculate_age_bonus(
            age,
            sport
        )


        percent = int(
            max(
                55,
                min(
                    95,
                    percent
                )
            )
        )



        result.append(
            {
                "sport":sport,
                "percent":percent
            }
        )



    result.sort(
        key=lambda x:x["percent"],
        reverse=True
    )


    return result[:5]