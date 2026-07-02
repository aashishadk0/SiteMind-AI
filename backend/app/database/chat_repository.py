"""
Chat database operations.
"""

from backend.app.database.database import Database


class ChatRepository:

    def __init__(self):

        self.conn = Database.connect()

    def create_chat(
        self,
        user_id,
        title="New Chat"
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            INSERT INTO chats(
                user_id,
                title
            )

            VALUES(?,?)
            """,

            (user_id, title)

        )

        self.conn.commit()

        return cursor.lastrowid

    def save_message(
        self,
        chat_id,
        role,
        content
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            INSERT INTO messages(

                chat_id,

                role,

                content

            )

            VALUES(?,?,?)

            """,

            (
                chat_id,
                role,
                content
            )

        )

        self.conn.commit()

    def get_messages(
        self,
        chat_id
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            SELECT *

            FROM messages

            WHERE chat_id=?

            ORDER BY id

            """,

            (chat_id,)

        )

        return [

            dict(row)

            for row in cursor.fetchall()

        ]

    def get_user_chats(
        self,
        user_id
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            SELECT *

            FROM chats

            WHERE user_id=?

            ORDER BY updated_at DESC

            """,

            (user_id,)

        )

        return [

            dict(row)

            for row in cursor.fetchall()

        ]

    def rename_chat(
        self,
        chat_id,
        title
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            UPDATE chats

            SET

            title=?,

            updated_at=CURRENT_TIMESTAMP

            WHERE id=?

            """,

            (
                title,
                chat_id
            )

        )

        self.conn.commit()

    def delete_chat(
        self,
        chat_id
    ):

        cursor = self.conn.cursor()

        cursor.execute(

            "DELETE FROM messages WHERE chat_id=?",

            (chat_id,)

        )

        cursor.execute(

            "DELETE FROM chats WHERE id=?",

            (chat_id,)

        )

        self.conn.commit()

    def get_chat(self, chat_id):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            SELECT *

            FROM chats

            WHERE id=?
            """,

            (chat_id,)

        )

        row = cursor.fetchone()

        return dict(row) if row else None
    
    def update_title(
    self,
    chat_id,
    title
):

        cursor = self.conn.cursor()

        cursor.execute(

            """
            UPDATE chats

            SET

            title=?,

            updated_at=CURRENT_TIMESTAMP

            WHERE id=?

            """,

            (
                title,
                chat_id
            )

        )

        self.conn.commit()