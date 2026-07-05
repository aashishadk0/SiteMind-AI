from backend.app.rag.retriever import Retriever
from backend.app.rag.prompt_builder import PromptBuilder
from backend.app.services.llm_service import LLMService
from backend.app.core.model_manager import ModelManager
from backend.app.database.chat_repository import ChatRepository
from backend.app.database.knowledge_repository import KnowledgeRepository
from backend.app.services.router_service import RouterService


class ChatService:
    def __init__(self):
        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.repository = ChatRepository()
        self.knowledge_repo = KnowledgeRepository()

    def make_title(self, question: str):
        title = question.strip().replace("\n", " ")

        if len(title) > 42:
            title = title[:42] + "..."

        return title or "New Chat"

    def generate_reply(self, chat_id, user_id, question, provider, model, source_id=None):
        full_answer = ""

        for token in self.generate_reply_stream(
            chat_id=chat_id,
            user_id=user_id,
            question=question,
            provider=provider,
            model=model,
            source_id=source_id
        ):
            full_answer += token

        return {
            "answer": full_answer.strip(),
            "sources": [],
        }

    def generate_reply_stream(self, chat_id, user_id, question, provider, model, source_id=None):
        if not ModelManager.is_valid(provider, model):
            raise ValueError("Invalid model selected.")

        previous_messages = self.repository.get_messages(chat_id)

        if len(previous_messages) == 0:
            self.repository.update_title(
                chat_id,
                self.make_title(question),
            )

        self.repository.save_message(chat_id, "user", question)

        route = RouterService.process(question)

        if route["handled"]:
            answer = route["answer"]
            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        sources = self.knowledge_repo.list_sources(user_id)

        if not sources:
            answer = "I don't have any indexed knowledge yet. Add a website URL first, and then I can answer questions from its content."
            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        if not source_id:
            answer = "Please select a knowledge source before asking a question."
            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        selected_source = self.knowledge_repo.get_source(source_id, user_id)

        if not selected_source:
            answer = "The selected knowledge source was not found in your account."
            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        if selected_source["status"] != "ready":
            answer = "This knowledge source is still being indexed. Please wait until indexing is complete."
            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        language = route.get("language", "english")

        chunks = self.retriever.retrieve(
            question=question,
            top_k=3,
            user_id=user_id,
            source_id=source_id
        )

        if not chunks:
            answer = (
                "म चयन गरिएको knowledge source मा यो जानकारी भेट्न सकिनँ।"
                if language == "nepali"
                else "I don't have enough information in the selected knowledge source to answer that."
            )

            self.repository.save_message(chat_id, "assistant", answer)
            yield answer
            return

        messages = self.prompt_builder.build(
            question=question,
            retrieved_chunks=chunks,
            history=previous_messages,
            language=language,
        )

        llm = LLMService(
            provider=provider,
            model=model,
        )

        full_answer = ""

        for token in llm.stream_chat(messages):
            full_answer += token
            yield token

        final_answer = full_answer.strip()

        self.repository.save_message(
            chat_id,
            "assistant",
            final_answer,
        )