# -*- coding: utf-8 -*-

"""
Sport Selector AI VK
VK Photos Upload V8.4

Загрузка фотографий спорта в VK
"""


import os
import json

import vk_api
from vk_api import VkUpload
from dotenv import load_dotenv



load_dotenv()


VK_TOKEN = os.getenv(
    "VK_TOKEN"
)


GROUP_ID = int(
    os.getenv(
        "VK_GROUP_ID"
    )
)



vk_session = vk_api.VkApi(
    token=VK_TOKEN
)


vk = vk_session.get_api()


upload = VkUpload(
    vk_session
)



# =====================================================
# ПАПКА С ФОТО
# =====================================================


IMAGE_FOLDER = "images"


SPORT_FILES = {


    "Дзюдо":
        "judo.jpg",


    "Самбо":
        "sambo.jpg",


    "Вольная борьба":
        "wrestling.jpg",


    "Бокс":
        "boxing.jpg",


    "ММА":
        "mma.jpg",


    "Спортивная акробатика":
        "acrobatics.jpg",


    "Прыжки на батуте":
        "trampoline.jpg",


    "Стрельба из лука":
        "archery.jpg",


    "Тяжёлая атлетика":
        "weightlifting.jpg"

}



# =====================================================
# ЗАГРУЗКА
# =====================================================


def upload_photo(
        filename
):


    path = os.path.join(
        IMAGE_FOLDER,
        filename
    )


    if not os.path.exists(path):

        print(
            "Нет файла:",
            path
        )

        return None



    photo = upload.photo_wall(
        path,
        group_id=GROUP_ID
    )


    item = photo[0]


    photo_id = (
        f"-{GROUP_ID}_"
        f"{item['id']}"
    )


    return photo_id




# =====================================================
# ОСНОВНАЯ ФУНКЦИЯ
# =====================================================


def upload_all():


    result = {}



    for sport, filename in SPORT_FILES.items():


        print(
            "Загрузка:",
            sport
        )


        photo_id = upload_photo(
            filename
        )


        if photo_id:


            result[sport] = photo_id



    with open(
        "sport_photos.json",
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=4
        )



    print(
        "Готово!"
    )



if __name__ == "__main__":

    upload_all()