from pydantic import BaseModel
from typing import Optional


class CreateFreeEmailDTO(BaseModel):
    account_id: str


class RefillDTO(BaseModel):
    email: str
    account_id: str


class GetExpireDTO(BaseModel):
    account_id: str
    email: str


class DeleteMailDTO(BaseModel):
    account_id: str
    email: str


class CreateQuotaDTO(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int


class UpdateQuotaDTO(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int