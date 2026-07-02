"""
Authentication Service
"""

import bcrypt

from backend.app.database.database import Database


class AuthService:

    def __init__(self):

        self.conn = Database.connect()

    def register(
        self,
        username,
        email,
        password
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            "SELECT id FROM users WHERE email=?",

            (email,)

        )

        if cursor.fetchone():

            raise ValueError(
                "Email already exists."
            )

        hashed = bcrypt.hashpw(

            password.encode(),

            bcrypt.gensalt()

        ).decode()

        cursor.execute(

            """
            INSERT INTO users(
                username,
                email,
                password
            )

            VALUES(?,?,?)
            """,

            (
                username,
                email,
                hashed
            )

        )

        self.conn.commit()

        return {

            "id": cursor.lastrowid,

            "username": username,

            "email": email

        }

    def login(
        self,
        email,
        password
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            SELECT *

            FROM users

            WHERE email=?
            """,

            (email,)

        )

        user = cursor.fetchone()

        if user is None:

            raise ValueError(
                "Invalid credentials."
            )

        if not bcrypt.checkpw(

            password.encode(),

            user["password"].encode()

        ):

            raise ValueError(
                "Invalid credentials."
            )

        return {

            "id": user["id"],

            "username": user["username"],

            "email": user["email"]

        }