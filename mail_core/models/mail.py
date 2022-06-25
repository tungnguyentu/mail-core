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


class ServiceResponseBase(BaseModel):
    message: Optional[str]


##
class MailCreateCommand(BaseModel):
    account_id: str
    password: Optional[str] = None


class MailRefillCommand(BaseModel):
    email: EmailStr
    account_id: str


class MailExpireCommand(BaseModel):
    account_id: str
    email: str

class CreateQuotaCommand(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int

class UpdateQuotaCommand(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int

##
class MailCreatePayload(UserModel):
    password: str
    domain_id: str


class MailRefillPayload(BaseModel):
    account_id: str
    email: EmailStr
    expire: int


class CreateQuotaPayload(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int


class UpdateQuotaPayload(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int


##
class MailCreateResponse(ServiceResponseBase):
    email: Optional[EmailStr]
    expire: Optional[int]


class MailRefillResponse(ServiceResponseBase):
    email: EmailStr
    expire: Optional[int]


class MailExpireResponse(ServiceResponseBase):
    remaining: Optional[int]


class MailDeleteResponse(ServiceResponseBase):
    account_id: Optional[str]
    email: Optional[str]


class MailCreateQuotaResponse(ServiceResponseBase):
    account_id: Optional[str]
    email_limit: Optional[int]
    custom_email_limit: Optional[int]
    alias_limit: Optional[int]


class MailUpdateQuotaResponse(ServiceResponseBase):
    account_id: Optional[str]
    email_limit: Optional[int]
    custom_email_limit: Optional[int]
    alias_limit: Optional[int]