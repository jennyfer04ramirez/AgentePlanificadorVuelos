from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Function Selection API")
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # cualquiera
    allow_credentials=True,
    allow_methods=["*"],      # GET, POST, PUT, DELETE, etc
    allow_headers=["*"],      # cualquiera
)