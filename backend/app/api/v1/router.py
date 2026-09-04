from fastapi import APIRouter

from app.api.v1.endpoints import datasets, health, mappings

api_router = APIRouter()
api_router.include_router(health.router, tags=["system"])
api_router.include_router(datasets.router, tags=["data"])
api_router.include_router(mappings.router, tags=["semantic-mapping"])
