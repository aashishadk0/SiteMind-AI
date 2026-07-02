"""
Basic guardrails and query routing.
"""

import re


class Guardrails:

    GREETINGS = {

        "hi",

        "hello",

        "hey",

        "good morning",

        "good afternoon",

        "good evening"

    }

    THANKS = {

        "thanks",

        "thank you",

        "thankyou",

        "thx"

    }

    GOODBYE = {

        "bye",

        "goodbye",

        "see you"

    }

    HARMFUL = [

        "make a bomb",

        "kill",

        "hack facebook",

        "malware",

        "ransomware"

    ]


    @staticmethod
    def classify(question: str):

        text = question.lower().strip()

        if not text:

            return "empty"

        if text in Guardrails.GREETINGS:

            return "greeting"

        if text in Guardrails.THANKS:

            return "thanks"

        if text in Guardrails.GOODBYE:

            return "goodbye"

        for keyword in Guardrails.HARMFUL:

            if keyword in text:

                return "blocked"

        return "rag"