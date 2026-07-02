"""
Model manager.
"""

from backend.app.core.model_registry import SUPPORTED_MODELS


class ModelManager:

    @staticmethod
    def get_all():

        return SUPPORTED_MODELS

    @staticmethod
    def get_provider(provider):

        return SUPPORTED_MODELS.get(provider)

    @staticmethod
    def is_valid(provider, model):

        provider_info = SUPPORTED_MODELS.get(provider)

        if not provider_info:

            return False

        valid_models = [

            item["id"]

            for item in provider_info["models"]

        ]

        return model in valid_models

    @staticmethod
    def default_model(provider):

        return SUPPORTED_MODELS[provider]["default"]