"""
Prompt Builder
"""

class PromptBuilder:

    SYSTEM_PROMPT = """
You are SiteMind AI.

Rules:

1. Answer ONLY from the provided context.
2. Never hallucinate.
3. If answer is unavailable, say:
'I couldn't find that information in the knowledge base.'
4. Greetings should be natural.
5. Keep answers concise.
"""

    def build(
        self,
        question: str,
        retrieved_chunks: list,
        history: list
    ):

        messages = []

        messages.append({
            "role": "system",
            "content": self.SYSTEM_PROMPT
        })

        # Previous conversation
        for msg in history:

            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        context = ""

        for chunk in retrieved_chunks:

            context += f"""

Website:
{chunk['website']}

Page:
{chunk['title']}

Content:
{chunk['content']}

-----------------------------
"""

        messages.append({

            "role": "user",

            "content": f"""
Knowledge Base

{context}

Current Question

{question}
"""
        })

        return messages