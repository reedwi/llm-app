from pydantic import BaseModel, Field
from typing import Optional

class SupaChatbotTrainingHook(BaseModel):
    type: str
    table: str
    record: dict
    schema_name: Optional[str] = Field(..., alias='schema')
    old_record: Optional[str]

class SupaPersonalChatbotHook(BaseModel):
    type: str
    table: str
    record: dict
    schema_name: Optional[str] = Field(..., alias='schema')
    old_record: Optional[dict]