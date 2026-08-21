# -*- coding: utf-8 -*-

"""
database.py V8.4 FINAL
База данных VK Sport Selector AI Bot
"""

import sqlite3


DB_NAME = "sport_selector.db"


# =====================================================
# Подключение к БД
# =====================================================

def get_connection():
    return sqlite3.connect(DB_NAME)



# =====================================================
# Нормализация ID пользователя
# =====================================================

def normalize_user_id(user):

    if isinstance(user, dict):

        return (
            user.get("user_id")
            or user.get("id")
            or user.get("vk_id")
        )

    return user



# =====================================================
# Создание таблицы
# =====================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY,

        age TEXT DEFAULT '',
        gender TEXT DEFAULT '',

        height TEXT DEFAULT '',
        weight TEXT DEFAULT '',

        activity TEXT DEFAULT '',

        speed TEXT DEFAULT '',
        strength TEXT DEFAULT '',
        coordination TEXT DEFAULT '',
        endurance TEXT DEFAULT '',
        flexibility TEXT DEFAULT '',
        competition TEXT DEFAULT '',
        contact TEXT DEFAULT '',

        step INTEGER DEFAULT 0

    )
    """)


    conn.commit()
    conn.close()



# =====================================================
# Создать пользователя
# =====================================================

def create_user(user_id):

    user_id = normalize_user_id(user_id)

    if user_id is None:
        return


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO users(user_id)
        VALUES(?)
        """,
        (
            int(user_id),
        )
    )


    conn.commit()
    conn.close()



# =====================================================
# Сохранить ответ
# =====================================================

def save_user(user_id, field, value):

    user_id = normalize_user_id(user_id)


    if user_id is None:
        return


    create_user(user_id)


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        f"""
        UPDATE users
        SET {field}=?
        WHERE user_id=?
        """,
        (
            str(value),
            int(user_id)
        )
    )


    conn.commit()
    conn.close()



# =====================================================
# Совместимость
# =====================================================

def update_user(user_id, field, value):

    save_user(
        user_id,
        field,
        value
    )



# =====================================================
# Получить данные пользователя
# =====================================================

def get_user(user_id, field=None):

    user_id = normalize_user_id(user_id)


    if user_id is None:
        return None


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE user_id=?
        """,
        (
            int(user_id),
        )
    )


    row = cursor.fetchone()


    conn.close()


    if row is None:
        return None



    columns = [

        "user_id",

        "age",
        "gender",

        "height",
        "weight",

        "activity",

        "speed",
        "strength",
        "coordination",
        "endurance",
        "flexibility",
        "competition",
        "contact",

        "step"
    ]


    data = dict(
        zip(
            columns,
            row
        )
    )


    if field:

        return data.get(field)


    return data



# =====================================================
# Шаг теста
# =====================================================

def get_step(user_id):

    data = get_user(user_id)


    if not data:
        return 0


    return data.get(
        "step",
        0
    )



def set_step(user_id, step):

    user_id = normalize_user_id(user_id)


    create_user(user_id)


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE users
        SET step=?
        WHERE user_id=?
        """,
        (
            int(step),
            int(user_id)
        )
    )


    conn.commit()
    conn.close()



# =====================================================
# Очистка пользователя
# =====================================================

def clear_user(user_id):

    user_id = normalize_user_id(user_id)


    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM users
        WHERE user_id=?
        """,
        (
            int(user_id),
        )
    )


    conn.commit()
    conn.close()



# Старое имя
def reset_user(user_id):

    clear_user(user_id)



# =====================================================
# Старт базы
# =====================================================

init_db()