from pydantic import BaseModel, Field
from typing import List, Optional
class IssueModel(BaseModel):
    level: str  # error / warning
    message: str

class DocumentModel(BaseModel):
    name: str
    detected_type: Optional[str]
    size_kb: int

class ExtractedModel(BaseModel):
    contractor: Optional[str] = None
    amount: Optional[str] = None
    date: Optional[str] = None
    subject: Optional[str] = None

class CheckResponseSchema(BaseModel):
    check_id: str
    status: str
    status_label: str
    reason: Optional[str] = None
    issues: List[IssueModel] = []
    documents: List[DocumentModel] = []
    extracted: ExtractedModel
    checked_at: str