import logging

from transformers import pipeline
import bentoml
from huggingface_hub import scan_cache_dir

logger = logging.getLogger(__name__)

class HuggingFaceModelsService:

    @staticmethod
    async def import_model(task: str, model: str):
        try:
            # Validate task and model, and download the model
            logger.info(f"Importing model: {model} for task: {task}")
            hf_pipeline = pipeline(task=task, model=model)
            logger.info(f"Model {model} imported successfully for task {task}")

            # Save the model using BentoML
            logger.info(f"Saving model {model} to BentoML with task {task}")
            bentoml_model_name = f"{task}_{model.replace('/', '_')}"
            saved_model = bentoml.transformers.save_model(
                name=bentoml_model_name,
                pipeline=hf_pipeline,
            )
            logger.info(f"Model {model} saved successfully with BentoML name: {saved_model.tag}")

            # Delete the model from Hugging Face cache
            await HuggingFaceModelsService.delete_model_from_hfcache(model)
            logger.info(f"Model {model} deleted from Hugging Face cache")
        except Exception as e:
            logger.error(f"Error importing model: {e}")
            raise Exception(f"Error importing model: {e}")
        

    @staticmethod
    async def delete_model_from_hfcache():
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
                    revision_lists.append(revision)

            logger.info(f"Found {len(revision_lists)} revisions to delete from Hugging Face cache")
            cache_info.delete_revisions(revision_lists)

            logger.info("All models deleted from Hugging Face cache successfully.")
        except Exception as e:
            logger.error(f"Error deleting model: {e}")
            raise Exception(f"Error deleting model: {e}")