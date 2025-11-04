import os
from fastapi import APIRouter, FastAPI
import uvicorn
from presentation.controllers.template_controller import template_router
from presentation.controllers.groups_controller import group_router
from presentation.controllers.exams_controller import exams_router
from presentation.controllers.summary_controller import summary_router
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import JWTExtractorMiddleware

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

# Add JWT Extractor Middleware
app.add_middleware(JWTExtractorMiddleware)

root_router.include_router(template_router)
root_router.include_router(group_router)
root_router.include_router(exams_router)
root_router.include_router(summary_router)
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
