from typing import Literal
from pydantic import BaseModel

class ImportedFiles(BaseModel):
    name: str
    source: str
    groupType: str
    entries: int
    records: int
    type: Literal["csv", "pdf", "xlsx"]

