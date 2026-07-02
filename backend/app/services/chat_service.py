from backend.app.rag.retriever import Retriever
from backend.app.rag.prompt_builder import PromptBuilder
from backend.app.services.llm_service import LLMService
from backend.app.core.model_manager import ModelManager
from backend.app.database.chat_repository import ChatRepository
from backend.app.services.router_service import RouterService


class ChatService:
    def __init__(self):
        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.repository = ChatRepository()

    def make_title(self, question: str):
        title = question.strip().replace("\n", " ")

        if len(title) > 42:
            title = title[:42] + "..."

        return title or "New Chat"

    def generate_reply(self, chat_id, question, provider, model):
        full_answer = ""

        for token in self.generate_reply_stream(
            chat_id,
            question,
            provider,
            model,
        ):
            full_answer += token

        return {
            "answer": full_answer.strip(),
            "sources": [],
        }

    def generate_reply_stream(self, chat_id, question, provider, model):
        if not ModelManager.is_valid(provider, model):
            raise ValueError("Invalid model selected.")

        previous_messages = self.repository.get_messages(chat_id)

        if len(previous_messages) == 0:
            self.repository.update_title(
                chat_id,
                self.make_title(question),
            )

        self.repository.save_message(
            chat_id,
            "user",
            question,
        )

        route = RouterService.process(question)

        if route["handled"]:
            answer = route["answer"]

            self.repository.save_message(
                chat_id,
                "assistant",
                answer,
            )

            yield answer
            return

        chunks = self.retriever.retrieve(
            question,
            top_k=3,
        )

        messages = self.prompt_builder.build(
            question,
            chunks,
            previous_messages[-8:],
        )

        llm = LLMService(
            provider=provider,
            model=model,
        )

        full_answer = ""

        for token in llm.stream_chat(messages):
            full_answer += token
            yield token

        self.repository.save_message(
            chat_id,
            "assistant",
            full_answer.strip(),
        )