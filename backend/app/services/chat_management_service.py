"""
Chat Management Service
"""

from backend.app.database.chat_repository import ChatRepository


class ChatManagementService:

    def __init__(self):

        self.repo = ChatRepository()

    def create_chat(self, user_id):

        chat_id = self.repo.create_chat(user_id)

        return {

            "chat_id": chat_id,

            "title": "New Chat"

        }

    def get_chats(self, user_id):

        return self.repo.get_user_chats(user_id)

    def get_history(self, chat_id):

        return self.repo.get_messages(chat_id)

    def rename_chat(

        self,

        chat_id,

        title

    ):

        self.repo.update_title(

            chat_id,

            title

        )

        return {

            "message": "Chat renamed."

        }

    def delete_chat(self, chat_id):

        self.repo.delete_chat(chat_id)

        return {

            "message": "Chat deleted."

        }