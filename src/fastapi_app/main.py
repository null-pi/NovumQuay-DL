from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from huggingface_models.routes import router as huggingface_models_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Starting up...")
    yield
    # Code to run on shutdown
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(huggingface_models_router, prefix="/huggingface_models", tags=["huggingface_models"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)