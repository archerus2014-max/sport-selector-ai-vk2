from vk_api.keyboard import (
    VkKeyboard,
    VkKeyboardColor
)



def make_keyboard(buttons):

    kb = VkKeyboard(
        one_time=True
    )


    for b in buttons:

        kb.add_button(
            b,
            color=VkKeyboardColor.PRIMARY
        )


    return kb.get_keyboard()



def start_keyboard():

    return make_keyboard(
        [
            "🚀 Начать тест"
        ]
    )



def gender_keyboard():

    return make_keyboard(
        [
            "👦 Мальчик",
            "👧 Девочка"
        ]
    )



def rating_keyboard():

    return make_keyboard(
        [
            "1",
            "2",
            "3",
            "4",
            "5"
        ]
    )