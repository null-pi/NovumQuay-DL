from pydantic import BaseModel


class ModelRequest(BaseModel):
    task: str
    model: str