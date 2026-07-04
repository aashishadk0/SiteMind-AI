"""
Supported AI providers and models.
"""


SUPPORTED_MODELS = {
    "groq": {
        "default": "llama-3.1-8b-instant",
        "models": [
            {
                "id": "llama-3.1-8b-instant",
                "name": "Groq Llama 3.1 8B Instant",
                "description": "Fast cloud model"
            },
            {
                "id": "llama-3.3-70b-versatile",
                "name": "Groq Llama 3.3 70B",
                "description": "Better quality"
            }
        ]
    },
    "ollama": {
        "default": "llama3.2:latest",
        "models": [
            {
                "id": "llama3.2:latest",
                "name": "Ollama Llama 3.2",
                "description": "Fast local model"
            },
            {
                "id": "mistral:latest",
                "name": "Ollama Mistral",
                "description": "Balanced local model"
            },
            {
                "id": "llama3.1:8b",
                "name": "Ollama Llama 3.1 8B",
                "description": "Better local quality"
            }
        ]
    }
}