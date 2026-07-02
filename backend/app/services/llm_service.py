from groq import Groq
from ollama import Client

from backend.app.config import GROQ_API_KEY, OLLAMA_URL


class LLMService:
    def __init__(self, provider: str, model: str):
        self.provider = provider.lower()
        self.model = model

        if self.provider == "ollama":
            self.client = Client(host=OLLAMA_URL)

        elif self.provider == "groq":
            self.client = Groq(api_key=GROQ_API_KEY)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def chat(self, messages: list, temperature: float = 0.2):
        if self.provider == "ollama":
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options={
                    "temperature": temperature,
                    "num_predict": 220,
                    "num_ctx": 2048,
                },
            )

            return response["message"]["content"].strip()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stream=False,
        )

        return response.choices[0].message.content.strip()

    def stream_chat(self, messages: list, temperature: float = 0.2):
        if self.provider == "ollama":
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": temperature,
                    "num_predict": 220,
                    "num_ctx": 2048,
                },
            )

            for chunk in stream:
                content = chunk["message"]["content"]

                if content:
                    yield content

        elif self.provider == "groq":
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content

                if content:
                    yield content