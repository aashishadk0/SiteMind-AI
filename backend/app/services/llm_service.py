"""
LLM Service

Supports:
- Ollama
- Groq

Future:
- Gemini
"""

from groq import Groq
from ollama import Client

from backend.app.config import (
    GROQ_API_KEY,
    OLLAMA_URL,
)


class LLMService:

    def __init__(
        self,
        provider: str,
        model: str,
    ):

        self.provider = provider.lower()

        self.model = model

        if self.provider == "ollama":

            self.client = Client(
                host=OLLAMA_URL
            )

        elif self.provider == "groq":

            self.client = Groq(
                api_key=GROQ_API_KEY
            )

        else:

            raise ValueError(
                f"Unsupported provider: {provider}"
            )

    def chat(
        self,
        messages: list,
        temperature: float = 0.2,
        stream = False
    ):

        if self.provider == "ollama":

            return self._chat_ollama(
                messages,
                temperature,
                stream
            )

        elif self.provider == "groq":

            return self._chat_groq(
                messages,
                temperature,
                stream
            )

    def _chat_ollama(
    self,
    messages,
    temperature,
    stream=False
):

        response = self.client.chat(

            model=self.model,

            messages=messages,

            stream=stream,

            options={

                "temperature": temperature,

                "num_predict": 180

            }

        )

        if stream:

            for chunk in response:

                content = chunk["message"]["content"]

                if content:

                    yield content

        else:

            return response["message"]["content"]    

    def _chat_groq(
    self,
    messages,
    temperature,
    stream=False
):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=messages,

            temperature=temperature,

            stream=stream,

        )

        if stream:

            for chunk in response:

                delta = chunk.choices[0].delta.content

                if delta:

                    yield delta

        else:

            return response.choices[0].message.content