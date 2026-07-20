from typing import Optional
from pydantic import BaseModel


class SubjectRequest(BaseModel):
    uuid: Optional[str]
    subject_name: str
    subject_description: str
    blocks: list[dict]  # теперь просто список словарей
    archives: str  # base64 строка


class TaskResponse(BaseModel):
    uuid: str
    status: str
    result_queue: str


class ResultResponse(BaseModel):
    uuid: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
