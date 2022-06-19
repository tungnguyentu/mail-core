from pydantic import BaseModel, EmailStr
from typing import Optional


class UserModel(BaseModel):
    account_id: str
    email: EmailStr
    init_at: int
    expire: int


class DomainModel(BaseModel):
    name: str
    domain_id: int


class QuotaModel(BaseModel):
    account_id: str
    email_limit: Optional[int] = None
    custom_email_limit: Optional[int] = None
    alias_limit: Optional[int] = None


class MailCreatePayload(UserModel):
    password: str
    domain_id: str


class ServiceResponseBase(BaseModel):
    message: str


class MailCreateResponse(ServiceResponseBase):
    email: Optional[EmailStr]
    expire: Optional[int]


class MailRefillPayload(BaseModel):
    email: EmailStr


class MailRefillResponse(ServiceResponseBase):
    email: EmailStr
    expire: int


class MailExpireResponse(ServiceResponseBase):
    expire: int
