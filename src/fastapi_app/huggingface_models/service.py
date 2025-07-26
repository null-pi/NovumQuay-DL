import logging

import bentoml
from huggingface_hub import scan_cache_dir

from model_format.service import ModelFormatService
from .dto import ModelFormat

logger = logging.getLogger(__name__)

class HuggingFaceModelsService:

    @staticmethod
    def check_model_exists(task: str, model: str) -> bool:
        """
        Check if a model exists in the Hugging Face Hub for a given task.
        """
        try:
            logger.info(f"Checking if model {model} exists for task {task}")
            bentoml_model_name = f"{task}_{model.replace('/', '_')}"
            
            return bentoml.models.get(bentoml_model_name) is not None
        except bentoml.exceptions.NotFound:
            logger.info(f"Model {model} does not exist for task {task}.")
            return False
        except Exception as e:
            logger.error(f"Error checking {model} for {task}: {e}")
            raise Exception(f"Error checking model: {e}")
        

    @staticmethod
    def import_model(**kwargs):
        try:
            task: str = kwargs.get("task", None)
            model: str = kwargs.get("model")
            format: ModelFormat = kwargs.get("format", ModelFormat.DEFAULT)
            gguf_filename: str = kwargs.get("gguf_filename", None)

            if model is None:
                raise ValueError("Model name must be provided.")

            if HuggingFaceModelsService.check_model_exists(task, model):
                logger.info(f"Model {model} already exists for task {task}. Skipping import.")
                return
            
            model_format_service = ModelFormatService(format)
            
            if format == ModelFormat.DEFAULT:
                saved_model = model_format_service.save_model(**kwargs)
                HuggingFaceModelsService.delete_model_from_hfcache()
            elif format == ModelFormat.GGUF:
                saved_model = model_format_service.save_model(**kwargs)
            else:
                raise ValueError(f"Unsupported model format: {format}")

            logger.info(f"Model {model} saved successfully with BentoML name: {saved_model.tag}")

            # Delete the model from Hugging Face cache
            logger.info(f"Model {model} deleted from Hugging Face cache")
        except Exception as e:
            logger.error(f"Error importing model: {e}")
            raise Exception(f"Error importing model: {e}")
        

    @staticmethod
    def delete_model_from_hfcache():
        try:
            # Scan the Hugging Face cache directory to get all models
            logger.info("Scanning Hugging Face cache directory for models")
            cache_info = scan_cache_dir()
            
            if not cache_info.repos:
                logger.info("No models found in Hugging Face cache.")
                return
            
            # Collect all revisions from the cache
            logger.info(f"Found {len(cache_info.repos)} repositories in Hugging Face cache")

            revision_lists = []
            for repo in cache_info.repos:
                for revision in repo.revisions:
                    revision_lists.append(revision.commit_hash)

            logger.info(f"Found {len(revision_lists)} revisions to delete from Hugging Face cache")
            cache_info.delete_revisions(*revision_lists).execute()

            logger.info("All models deleted from Hugging Face cache successfully.")
        except Exception as e:
            logger.error(f"Error deleting model: {e}")
            raise Exception(f"Error deleting model: {e}")