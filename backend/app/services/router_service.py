from backend.app.core.guardrails import Guardrails


class RouterService:
    @staticmethod
    def process(question):
        category = Guardrails.classify(question)
        is_nepali = Guardrails.is_nepali(question)

        if category == "greeting":
            return {
                "handled": True,
                "answer": "Hello! Add a website URL first, then I can answer questions from its indexed content."
            }

        if category == "thanks":
            return {
                "handled": True,
                "answer": "You're welcome."
            }

        if category == "acknowledgement":
            return {
                "handled": True,
                "answer": "You can ask a specific question from the selected knowledge source."
            }

        if category == "empty":
            return {
                "handled": True,
                "answer": "Please enter a question."
            }

        if category == "blocked":
            return {
                "handled": True,
                "answer": "I can't help with that. I only answer questions from the indexed knowledge base."
            }

        return {
            "handled": False,
            "language": "nepali" if is_nepali else "english"
        }