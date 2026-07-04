import re


class Guardrails:
    GREETINGS = {
        "hi", "hello", "hey", "namaste", "नमस्ते",
        "good morning", "good afternoon", "good evening"
    }

    THANKS = {
        "thanks", "thank you", "thx", "धन्यवाद", "thankyou"
    }

    ACKNOWLEDGEMENTS = {
        "ok", "okay", "ayy", "hora", "ho ra", "ramro", "aw", "ehh",
        "hmm", "hajur", "la", "ठीक छ", "हो र", "अँ", "हुन्छ", "राम्रो"
    }

    BLOCKED_PATTERNS = [
        r"ignore previous",
        r"ignore all",
        r"system prompt",
        r"developer message",
        r"jailbreak",
        r"prompt injection",
        r"act as",
        r"pretend to",
        r"give me.*code",
        r"write.*code",
        r"python code",
        r"javascript code",
        r"make.*virus",
        r"hack",
        r"malware",
        r"phishing",
        r"ransomware",
        r"bomb",
    ]

    @staticmethod
    def is_nepali(text: str) -> bool:
        return bool(re.search(r"[\u0900-\u097F]", text))

    @staticmethod
    def classify(question: str):
        text = question.lower().strip()

        if not text:
            return "empty"

        if text in Guardrails.GREETINGS:
            return "greeting"

        if text in Guardrails.THANKS:
            return "thanks"

        if text in Guardrails.ACKNOWLEDGEMENTS:
            return "acknowledgement"

        for pattern in Guardrails.BLOCKED_PATTERNS:
            if re.search(pattern, text):
                return "blocked"

        return "rag"