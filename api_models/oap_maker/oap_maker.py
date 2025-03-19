from pydantic import BaseModel, ConfigDict, Field


class ImportOapProgram(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ExportOapProgram(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
