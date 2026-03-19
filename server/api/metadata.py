from pydantic import BaseModel

class ApiMetadata(BaseModel):
    importedFiles: int
    successfulMappings: int
    mappingAlerts: int
