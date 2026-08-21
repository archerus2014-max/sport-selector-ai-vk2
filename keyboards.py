# -*- coding: utf-8 -*-

"""
keyboards.py V9.1
Кнопки SPORT SELECTOR AI
"""

from vk_api.keyboard import VkKeyboard, VkKeyboardColor



# =====================================================
# Старт
# =====================================================

def start_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )

    keyboard.add_button(
        "🏁 Начать подбор спорта",
        color=VkKeyboardColor.PRIMARY
    )

    return keyboard.get_keyboard()



# =====================================================
# Пол
# =====================================================

def gender_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    keyboard.add_button(
        "👦 Мальчик",
        color=VkKeyboardColor.PRIMARY
    )


    keyboard.add_button(
        "👧 Девочка",
        color=VkKeyboardColor.POSITIVE
    )


    return keyboard.get_keyboard()



# =====================================================
# Активность
# =====================================================

def activity_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    buttons = [

        "Очень активный",
        "Средняя активность",
        "Спокойный ребенок"

    ]


    for item in buttons:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Сила
# =====================================================

def strength_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Слабый",
        "Средняя сила",
        "Сильный"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Скорость
# =====================================================

def speed_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Медленный",
        "Быстрый",
        "Очень быстрый"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Координация
# =====================================================

def coordination_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Менее координированный",
        "Средняя координация",
        "Хорошо координированный"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Выносливость
# =====================================================

def endurance_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Быстро устает",
        "Средняя выносливость",
        "Очень выносливый"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Гибкость
# =====================================================

def flexibility_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Негибкий",
        "Средняя гибкость",
        "Очень гибкий"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Соревновательность
# =====================================================

def competition_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Не любит соревнования",
        "Спокойно относится",
        "Любит побеждать"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Контакт
# =====================================================

def contact_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    for item in [

        "Избегает контакта",
        "Нейтрально",
        "Любит борьбу"

    ]:

        keyboard.add_button(
            item,
            color=VkKeyboardColor.PRIMARY
        )


    return keyboard.get_keyboard()



# =====================================================
# Результат
# =====================================================

def result_keyboard():

    keyboard = VkKeyboard(
        one_time=True
    )


    keyboard.add_button(
        "🔄 Пройти тест заново",
        color=VkKeyboardColor.PRIMARY
    )


    return keyboard.get_keyboard()