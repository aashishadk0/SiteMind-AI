from backend.app.core.guardrails import Guardrails


class RouterService:
    @staticmethod
    def process(question):
        category = Guardrails.classify(question)
        is_nepali = Guardrails.is_nepali(question)

        if category == "greeting":
            return {
                "handled": True,
                "answer": "नमस्ते! म indexed knowledge base बाट मात्र उत्तर दिन सक्छु।" if is_nepali else
                "Hello! I can answer questions from the indexed knowledge base."
            }

        if category == "thanks":
            return {
                "handled": True,
                "answer": "स्वागत छ।" if is_nepali else "You're welcome."
            }

        if category == "acknowledgement":
            return {
                "handled": True,
                "answer": "हो, तपाईं यसै विषयमा थप प्रश्न सोध्न सक्नुहुन्छ।" if is_nepali else
                "Yes, you can ask a more specific follow-up about this topic."
            }

        if category == "empty":
            return {
                "handled": True,
                "answer": "कृपया प्रश्न लेख्नुहोस्।" if is_nepali else "Please enter a question."
            }

        if category == "blocked":
            return {
                "handled": True,
                "answer": "म indexed knowledge base भित्रको जानकारी मात्र दिन सक्छु।" if is_nepali else
                "I can only answer questions related to the indexed knowledge base."
            }

        return {
            "handled": False,
            "language": "nepali" if is_nepali else "english"
        }