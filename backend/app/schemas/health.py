from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["decilyra-api"])


class SystemInfoResponse(BaseModel):
    service: str
    version: str
    environment: str
    database_configured: bool
    api_prefix: str


class WorkspaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
