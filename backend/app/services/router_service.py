"""
Simple query router.
"""

from backend.app.core.guardrails import Guardrails


class RouterService:

    @staticmethod
    def process(question):

        category = Guardrails.classify(question)

        if category == "greeting":

            return {

                "handled": True,

                "answer": "Hello! 👋 How can I help you today?"

            }

        if category == "thanks":

            return {

                "handled": True,

                "answer": "You're welcome! 😊"

            }

        if category == "goodbye":

            return {

                "handled": True,

                "answer": "Goodbye! Have a great day."

            }

        if category == "empty":

            return {

                "handled": True,

                "answer": "Please enter a question."

            }

        if category == "blocked":

            return {

                "handled": True,

                "answer": "I can't assist with that request."

            }

        return {

            "handled": False

        }