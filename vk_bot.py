# -*- coding: utf-8 -*-

"""
Sport Selector AI VK
VK BOT V9 CLOUD

FastAPI + VK Callback API
"""


from fastapi import FastAPI, Request
import vk_api
import traceback


from config import (
    VK_TOKEN,
    CALLBACK_SECRET
)


from database import (
    create_user,
    get_user,
    save_user,
    reset_user
)


from engine import recommend


from cards import result_card


from keyboards import (
    gender_keyboard,
    rating_keyboard,
    start_keyboard
)



# =====================================================
# VK
# =====================================================


app = FastAPI()



vk_session = vk_api.VkApi(
    token=VK_TOKEN
)


vk = vk_session.get_api()



# =====================================================
# ВОПРОСЫ
# =====================================================


questions = [

    ("age",
     "Введите возраст ребёнка:"),

    ("gender",
     "Выберите пол ребёнка:"),

    ("height",
     "Введите рост ребёнка (см):"),

    ("weight",
     "Введите вес ребёнка (кг):"),


    ("coordination",
     "Оцените координацию 1-5"),

    ("speed",
     "Оцените скорость 1-5"),

    ("strength",
     "Оцените силу 1-5"),

    ("endurance",
     "Оцените выносливость 1-5"),

    ("flexibility",
     "Оцените гибкость 1-5"),

    ("balance",
     "Оцените равновесие 1-5"),


    ("competition",
     "Любит соревнования? 1-5"),

    ("discipline",
     "Дисциплинированность 1-5"),

    ("activity",
     "Активность ребёнка 1-5"),

    ("contact",
     "Любит контактные игры? 1-5"),

    ("focus",
     "Концентрация внимания 1-5")

]



# =====================================================
# ОТПРАВКА
# =====================================================


def send(
        user_id,
        text,
        keyboard=None
):

    vk.messages.send(

        user_id=user_id,

        message=text,

        keyboard=keyboard,

        random_id=0

    )



# =====================================================
# НАЧАЛО
# =====================================================


def start_test(
        user_id
):

    create_user(
        user_id
    )


    send(

        user_id,

"""
🏆 AI-подбор спорта для ребёнка


Определим наиболее подходящие
спортивные направления.


Начинаем тест!
""",

        start_keyboard()

    )



# =====================================================
# СЛЕДУЮЩИЙ ВОПРОС
# =====================================================


def next_question(
        user_id,
        step
):


    key,text = questions[step]



    if key=="gender":

        send(
            user_id,
            text,
            gender_keyboard()
        )

        return



    if key in [

        "coordination",
        "speed",
        "strength",
        "endurance",
        "flexibility",
        "balance",
        "competition",
        "discipline",
        "activity",
        "contact",
        "focus"

    ]:

        send(
            user_id,
            text,
            rating_keyboard()
        )

        return



    send(
        user_id,
        text
    )



# =====================================================
# РЕЗУЛЬТАТ
# =====================================================


def finish(
        user_id,
        data
):


    result = recommend(
        data
    )


    text=result_card(

        result,

        data.get(
            "age",
            ""
        )

    )


    send(
        user_id,
        text
    )


    reset_user(
        user_id
    )



# =====================================================
# WEB
# =====================================================


@app.get("/")

def home():

    return {

        "status":
        "Sport Selector AI VK V9 Cloud"

    }



# =====================================================
# CALLBACK VK
# =====================================================


@app.post("/callback")
async def callback(
        request:Request
):


    try:


        data = await request.json()



        # проверка VK

        if data.get(
            "secret"
        ) != CALLBACK_SECRET:

            return "ok"



        event_type=data.get(
            "type"
        )



        # подтверждение сервера

        if event_type=="confirmation":


            return "c7bacebd"



        # сообщение

        if event_type=="message_new":


            message=data["object"]["message"]


            user_id=message["from_id"]


            text=message["text"].strip()



            if text.lower() in [

                "старт",
                "начать",
                "/start"

            ]:


                start_test(
                    user_id
                )

                return "ok"




            user=get_user(
                user_id
            )



            if not user:


                send(

                    user_id,

                    "Нажмите «Начать»"

                )


                return "ok"




            step=user["step"]

            data=user["data"]



            if step>=len(questions):


                finish(
                    user_id,
                    data
                )


                return "ok"




            field,_=questions[step]



            if field in [

                "age",
                "height",
                "weight"

            ]:


                data[field]=int(text)



            elif field=="gender":


                data[field]=text



            else:


                if "answers" not in data:

                    data["answers"]={}


                data["answers"][field]=int(text)



            step+=1



            if step<len(questions):


                save_user(

                    user_id,

                    step,

                    data

                )


                next_question(

                    user_id,

                    step

                )



            else:


                finish(

                    user_id,

                    data

                )



        return "ok"



    except Exception:


        traceback.print_exc()


        return "ok"