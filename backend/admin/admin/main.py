import os

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from admin.infrastructure.web.middlewares.jwt_extractor import JWTExtractorMiddleware
from admin.infrastructure.web.routes.exams_router import exams_router
from admin.infrastructure.web.routes.groups_routes import group_router
from admin.infrastructure.web.routes.summary_routes import summary_router
from admin.infrastructure.web.routes.templates_router import template_router

origins = ["*"]

root_router = APIRouter(prefix="/manager")

app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(JWTExtractorMiddleware)

# routers
root_router.include_router(group_router)
root_router.include_router(exams_router)
root_router.include_router(summary_router)
root_router.include_router(template_router)

app.include_router(root_router)


def run_fastapi():
    # Load .env if present, but don't override existing environment variables
    load_dotenv(override=False)
    port = int(os.getenv("PORT", 8081))
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,
        access_log=False,
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    run_fastapi()
