# -*- coding: utf-8 -*-

"""
API для VK Mini App
Спортивный агент
"""


from flask import Flask, request, jsonify
from flask_cors import CORS


from engine import recommend



app = Flask(__name__)


CORS(app)



# =====================================================
# Проверка работы
# =====================================================

@app.route("/")
def home():

    return {

        "status":"ok",

        "message":
        "Спортивный агент работает"

    }




# =====================================================
# Получение анкеты ребенка
# =====================================================

@app.route(
    "/recommend",
    methods=["POST"]
)

def get_recommendation():


    try:


        data = request.json



        result = recommend(
            data
        )



        return jsonify({

            "success":True,

            "result":result

        })



    except Exception as e:



        return jsonify({

            "success":False,

            "error":str(e)

        })





# =====================================================
# Запуск
# =====================================================


if __name__ == "__main__":


    print(
"""
====================================
🏆 СПОРТИВНЫЙ АГЕНТ API
Запущен
====================================
"""
    )



    app.run(

        host="0.0.0.0",

        port=5000

    )