from fastapi import FastAPI
from src.api.routes import router as tax_router

app = FastAPI(
    title="Personal Finance Tax Agent API",
    version="1.0.0"
)

app.include_router(tax_router)
