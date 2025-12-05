import os
from fastapi import APIRouter, FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

root_router = APIRouter(prefix="/manager")

app = FastAPI(docs_url="/docs",
              redoc_url="/redoc",
              openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(root_router)
def run_fastapi():
    port = int(os.getenv("PORT", 8081))
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
        access_log=True,
    )
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    run_fastapi()
