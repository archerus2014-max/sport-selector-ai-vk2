# -*- coding: utf-8 -*-

"""
SPORT SELECTOR AI VK BOT V9.1

Анкета:
1. Возраст (число)
2. Рост (число)
3. Вес (число)
4. Пол
5. Активность
6. Сила
7. Скорость
8. Координация
9. Выносливость
10. Гибкость
11. Соревновательность
12. Контакт
"""

import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


from keyboards import (
    start_keyboard,
    gender_keyboard,
    activity_keyboard,
    strength_keyboard,
    speed_keyboard,
    coordination_keyboard,
    endurance_keyboard,
    flexibility_keyboard,
    competition_keyboard,
    contact_keyboard,
    result_keyboard
)


from database import (
    create_user,
    save_user,
    get_user,
    set_step,
    get_step,
    reset_user
)


from engine import recommend



# =====================================================
# VK
# =====================================================

load_dotenv()


VK_TOKEN = os.getenv("VK_TOKEN")


if not VK_TOKEN:

    print("VK_TOKEN не найден")

    exit()



vk_session = vk_api.VkApi(
    token=VK_TOKEN
)


vk = vk_session.get_api()


longpoll = VkLongPoll(
    vk_session
)



# =====================================================
# Отправка сообщения
# =====================================================

def send_message(
        user_id,
        text,
        keyboard=None
):

    vk.messages.send(

        user_id=user_id,

        message=text,

        random_id=0,

        keyboard=keyboard

    )



# =====================================================
# Начало теста
# =====================================================

def start_test(user_id):

    create_user(user_id)

    set_step(
        user_id,
        1
    )


    send_message(
        user_id,
        """
🏆 SPORT SELECTOR AI

Определим подходящий вид спорта для ребенка.

Введите возраст ребенка цифрой.

Например:
8
""",
    )



# =====================================================
# Обработка ответов
# =====================================================

def process_answer(
        user_id,
        text
):

    step = get_step(user_id)



    # -----------------------------
    # Возраст
    # -----------------------------

    if step == 1:


        if not text.isdigit():

            send_message(
                user_id,
                "Введите возраст только цифрой."
            )

            return



        save_user(
            user_id,
            "age",
            text
        )


        set_step(
            user_id,
            2
        )


        send_message(
            user_id,
            "Введите рост ребенка в сантиметрах.\nНапример: 135"
        )


        return



    # -----------------------------
    # Рост
    # -----------------------------

    if step == 2:


        if not text.isdigit():

            send_message(
                user_id,
                "Введите рост цифрой. Например: 135"
            )

            return



        save_user(
            user_id,
            "height",
            text
        )


        set_step(
            user_id,
            3
        )


        send_message(
            user_id,
            "Введите вес ребенка в килограммах.\nНапример: 30"
        )


        return



    # -----------------------------
    # Вес
    # -----------------------------

    if step == 3:


        if not text.isdigit():

            send_message(
                user_id,
                "Введите вес цифрой. Например: 30"
            )

            return



        save_user(
            user_id,
            "weight",
            text
        )


        set_step(
            user_id,
            4
        )


        send_message(
            user_id,
            "Выберите пол ребенка:",
            gender_keyboard()
        )


        return



    # -----------------------------
    # Пол
    # -----------------------------

    if step == 4:


        save_user(
            user_id,
            "gender",
            text
        )


        set_step(
            user_id,
            5
        )


        send_message(
            user_id,
            "Какой уровень активности?",
            activity_keyboard()
        )


        return



    # -----------------------------
    # Активность
    # -----------------------------

    if step == 5:


        save_user(
            user_id,
            "activity",
            text
        )


        set_step(
            user_id,
            6
        )


        send_message(
            user_id,
            "Какая сила у ребенка?",
            strength_keyboard()
        )


        return



    # -----------------------------
    # Сила
    # -----------------------------

    if step == 6:


        save_user(
            user_id,
            "strength",
            text
        )


        set_step(
            user_id,
            7
        )


        send_message(
            user_id,
            "Какая скорость?",
            speed_keyboard()
        )


        return



    # -----------------------------
    # Скорость
    # -----------------------------

    if step == 7:


        save_user(
            user_id,
            "speed",
            text
        )


        set_step(
            user_id,
            8
        )


        send_message(
            user_id,
            "Как развита координация?",
            coordination_keyboard()
        )


        return



    # -----------------------------
    # Координация
    # -----------------------------

    if step == 8:


        save_user(
            user_id,
            "coordination",
            text
        )


        set_step(
            user_id,
            9
        )


        send_message(
            user_id,
            "Какая выносливость?",
            endurance_keyboard()
        )


        return



    # -----------------------------
    # Выносливость
    # -----------------------------

    if step == 9:


        save_user(
            user_id,
            "endurance",
            text
        )


        set_step(
            user_id,
            10
        )


        send_message(
            user_id,
            "Какая гибкость?",
            flexibility_keyboard()
        )


        return



    # -----------------------------
    # Гибкость
    # -----------------------------

    if step == 10:


        save_user(
            user_id,
            "flexibility",
            text
        )


        set_step(
            user_id,
            11
        )


        send_message(
            user_id,
            "Отношение к соревнованиям?",
            competition_keyboard()
        )


        return



    # -----------------------------
    # Соревнования
    # -----------------------------

    if step == 11:


        save_user(
            user_id,
            "competition",
            text
        )


        set_step(
            user_id,
            12
        )


        send_message(
            user_id,
            "Отношение к контакту и борьбе?",
            contact_keyboard()
        )


        return



    # -----------------------------
    # Контакт
    # -----------------------------

    if step == 12:


        save_user(
            user_id,
            "contact",
            text
        )


        data = get_user(
            user_id
        )


        result = recommend(
            data
        )


        send_message(
            user_id,
            result,
            result_keyboard()
        )


        set_step(
            user_id,
            0
        )


        return



# =====================================================
# Запуск
# =====================================================

print(
"""
==================================================
SPORT SELECTOR AI VK BOT V9.1
Запущен
==================================================
"""
)



for event in longpoll.listen():


    if event.type == VkEventType.MESSAGE_NEW and event.to_me:


        user_id = event.user_id

        text = event.text.strip()



        print(
            user_id,
            ":",
            text
        )



        try:


            if text.lower() in [

                "старт",
                "start",
                "начать",
                "🏁 Начать подбор спорта"

            ]:


                start_test(
                    user_id
                )



            elif text.lower() in [

                "заново",
                "сброс"

            ]:


                reset_user(
                    user_id
                )


                start_test(
                    user_id
                )



            else:


                process_answer(
                    user_id,
                    text
                )



        except Exception as e:


            print(
                "Ошибка:",
                e
            )


            send_message(
                user_id,
                "Ошибка обработки. Напишите: старт"
            )