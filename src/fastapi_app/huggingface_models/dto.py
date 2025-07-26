import enum
from typing import Optional
from pydantic import BaseModel
import transformers


class ModelFormat(str, enum.Enum):
    DEFAULT = "default"
    GGUF = "gguf"


class ModelRequest(BaseModel):
    task: Optional[str] = None
    model: str
    format: ModelFormat = ModelFormat.DEFAULT
    gguf_filename: Optional[str] = None
