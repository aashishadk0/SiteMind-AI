"""
Supported AI providers and models.
"""


SUPPORTED_MODELS = {

    "ollama": {

        "default": "llama3.1:8b",

        "models": [

            {
                "id": "llama3.1:8b",
                "name": "Llama 3.1 8B",
                "description": "Best overall local model"
            },

            {
                "id": "mistral:latest",
                "name": "Mistral",
                "description": "Fast local model"
            },

            {
                "id": "llama3.2:latest",
                "name": "Llama 3.2",
                "description": "Small and efficient"
            }

        ]

    },

    "groq": {

        "default": "llama-3.3-70b-versatile",

        "models": [

            {
                "id": "llama-3.3-70b-versatile",
                "name": "Llama 3.3 70B",
                "description": "Best quality"
            },

            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B Instant",
                "description": "Very fast"
            }

        ]

    }

}