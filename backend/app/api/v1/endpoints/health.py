from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse, SystemInfoResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="decilyra-api")


@router.get("/system", response_model=SystemInfoResponse)
def system_info() -> SystemInfoResponse:
    settings = get_settings()
    return SystemInfoResponse(
        service="decilyra-api",
        version="0.1.0",
        environment=settings.environment,
        database_configured=bool(settings.database_url),
        api_prefix=settings.api_v1_prefix,
    )
