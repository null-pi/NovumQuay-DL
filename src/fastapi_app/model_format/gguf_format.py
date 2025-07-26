import logging
import os
import requests
import shutil
import tempfile

from llama_cpp import Llama
import bentoml

from .interface import ModelFormatInterface

logger = logging.getLogger(__name__)

class GGUFModelFormat(ModelFormatInterface):
    def __download_gguf_http__(self, model: str, gguf_filename: str, dest_dir: str):
        try:
            logger.info(f"Downloading GGUF model {model} from Hugging Face Hub")
            
            url = f"https://huggingface.co/{model}/resolve/main/{gguf_filename}"
            dest_path = os.path.join(dest_dir, gguf_filename)

            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

            logger.info(f"GGUF model downloaded to {dest_path}")

            return dest_path
        except Exception as e:
            logger.error(f"Error downloading GGUF model: {e}")
            raise Exception(f"Error downloading GGUF model: {e}")
        

    def save_model(self, **kwargs):
        try:
            model: str = kwargs.get("model")
            gguf_filename: str = kwargs.get("gguf_filename")

            if model is None or gguf_filename is None:
                raise ValueError("Model name and GGUF filename must be provided.")

            logger.info(f"Using GGUF format for model {model}")

            with tempfile.TemporaryDirectory() as temp_dir:
                # Download the GGUF model file
                gguf_path = self.__download_gguf_http__(model, gguf_filename, temp_dir)
            
                llm = Llama(model_path=gguf_path)

                # Save the model using BentoML
                logger.info(f"Saving model {model} to BentoML with GGUF format {gguf_filename}")
                bentoml_model_name = f"{model.replace('/', '_')}"
                
                saved_model = None 

                with bentoml.models.create(
                    name=bentoml_model_name
                ) as bentoml_model_ref:
                    # Save the GGUF model to BentoML
                    dest_path = os.path.join(bentoml_model_ref.path, gguf_filename)
                    shutil.copy(gguf_path, dest_path)
                    logger.info(f"GGUF model {gguf_filename} copied to BentoML path {dest_path}")

                    saved_model = bentoml_model_ref

            return saved_model
        except Exception as e:
            logger.error(f"Error in GGUF format: {e}")
            raise Exception(f"Error in GGUF format: {e}")