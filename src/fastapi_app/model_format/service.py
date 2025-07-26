import logging

from huggingface_models.dto import ModelFormat
from .default_format import DefaultModelFormat
from .gguf_format import GGUFModelFormat


logger = logging.getLogger(__name__)

class ModelFormatService:
    def __init__(self, format: ModelFormat):
        self.format = format
        self.format_instance = self.__function_router__()


    def __function_router__(self):
        try:
            if self.format == ModelFormat.DEFAULT:
                return DefaultModelFormat()
            elif self.format == ModelFormat.GGUF:
                return GGUFModelFormat()
            else:
                raise ValueError(f"Unsupported model format: {self.format}")
        except Exception as e:
            logger.error(f"Error in function router: {e}")
            raise Exception(f"Error in function router: {e}")
        

    def save_model(self, **kwargs):
        """
        Call the appropriate function based on the model format.
        """
        try:
            return self.format_instance.save_model(**kwargs)
        except Exception as e:
            logger.error(f"Error calling function for task: {e}")
            raise Exception(f"Error calling function: {e}")