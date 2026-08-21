# -*- coding:utf-8 -*-

import sqlite3
import json
import os


DB = "sport_ai.db"


conn = sqlite3.connect(
    DB,
    check_same_thread=False
)


cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS users
(
id INTEGER PRIMARY KEY,

step INTEGER DEFAULT 0,

data TEXT

)
""")


conn.commit()



def get_user(user_id):

    cursor.execute(
        """
        SELECT step,data
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )

    row = cursor.fetchone()


    if not row:

        return None


    return {

        "step": row[0],

        "data":
        json.loads(row[1])

    }



def create_user(user_id):

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        VALUES
        (
        ?,
        0,
        '{}'
        )
        """,
        (user_id,)
    )


    conn.commit()



def save_user(
        user_id,
        step,
        data
):

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        VALUES
        (?,?,?)
        """,
        (
            user_id,
            step,
            json.dumps(
                data,
                ensure_ascii=False
            )
        )
    )


    conn.commit()



def reset_user(user_id):

    create_user(user_id)