import os
import time

from fastapi import APIRouter, FastAPI, Request
import uvicorn
from presentation.controllers.template_controller import template_router
from presentation.controllers.groups_controller import group_router

base = "manager"
root = APIRouter(prefix=f"/{base}")

app = FastAPI(docs_url=f"/{base}/docs",
    redoc_url=f"/{base}/redoc",
    openapi_url=f"/{base}/openapi.json")


root.include_router(template_router)
root.include_router(group_router)
app.include_router(root)


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