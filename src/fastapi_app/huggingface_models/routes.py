import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from .service import HuggingFaceModelsService
from .dto import ModelRequest


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/import")
async def import_model(body: ModelRequest):
    try:
        HuggingFaceModelsService.import_model(**body.model_dump()) 

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Model {body.model} imported successfully for task {body.task}"
            }
        )
    except Exception as e:
        logger.error(f"Error importing model: {e}")
        raise HTTPException(status_code=500, detail=f"Error importing model: {e}")