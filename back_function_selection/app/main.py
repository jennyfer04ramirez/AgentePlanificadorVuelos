from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Function Selection API")
app.include_router(router)
