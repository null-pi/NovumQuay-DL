import logging

from transformers import pipeline
import bentoml

from .interface import ModelFormatInterface

logger = logging.getLogger(__name__)

class DefaultModelFormat(ModelFormatInterface):
    def save_model(self, **kwargs):
        try:
            task: str = kwargs.get("task")
            model: str = kwargs.get("model")

            if task is None or model is None:
                raise ValueError("Task and model must be provided.")

            logger.info(f"Using default format for task {task} and model {model}")
            # Validate task and model, and download the model
            logger.info(f"Downloading model: {model} for task: {task}")
            hf_pipeline = pipeline(task=task, model=model)
            logger.info(f"Model {model} imported successfully for task {task}")

            # Save the model using BentoML
            logger.info(f"Saving model {model} to BentoML with task {task}")
            bentoml_model_name = f"{model.replace('/', '_')}"
            
            saved_model = None 

            with bentoml.models.create(
                name=bentoml_model_name
            ) as bentoml_model_ref:
                hf_pipeline.save_pretrained(bentoml_model_ref.path)
                saved_model = bentoml_model_ref

            return saved_model
        except Exception as e:
            logger.error(f"Error in default format: {e}")
            raise Exception(f"Error in default format: {e}")