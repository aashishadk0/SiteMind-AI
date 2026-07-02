"""
Main RAG chat service.
"""

from backend.app.database.chat_repository import ChatRepository
from backend.app.rag.retriever import Retriever
from backend.app.rag.prompt_builder import PromptBuilder
from backend.app.services.llm_service import LLMService
from backend.app.core.model_manager import ModelManager
from backend.app.services.router_service import RouterService

class ChatService:

    def __init__(self):

        self.retriever = Retriever()

        self.repository = ChatRepository()

        self.prompt_builder = PromptBuilder()

    def generate_reply(

        self,

        chat_id,

        question,

        provider,

        model,

    ):

        if not ModelManager.is_valid(
            provider,
            model
        ):
            raise ValueError("Invalid model.")

        # Save user message
        self.repository.save_message(

            chat_id,

            "user",

            question

        )

        # Load conversation history
        history = self.repository.get_messages(
            chat_id
        )

        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(

            question,

            top_k=3

        )

        # Build prompt
        messages = self.prompt_builder.build(

            question,

            chunks,

            history

        )

        llm = LLMService(

            provider,

            model

        )

        answer = ""

        for piece in llm.chat(

            messages,

            stream=True

        ):

                answer += piece

        # Save assistant reply
        self.repository.save_message(

            chat_id,

            "assistant",

            answer

        )

        return {

            "answer": answer,

            "sources": chunks

        }