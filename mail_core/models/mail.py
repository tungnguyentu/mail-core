from pydantic import BaseModel, EmailStr
from typing import Optional, List


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


##
class MailGetQuotaCommand(BaseModel):
    account_id: str

class MailCreateFreeCommand(BaseModel):
    account_id: str


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


class GetEmailCommand(BaseModel):
    account_id: str
    email: EmailStr


class UpdateQuotaCommand(BaseModel):
    account_id: str
    email_limit: int
    custom_email_limit: int
    alias_limit: int

class GetEmailsCommand(BaseModel):
    account_id: str

class ActivateEmailCommand(BaseModel):
    account_id: str
    email: EmailStr


class CreateMailPremiumCommand(BaseModel):
    account_id: str
    username: str
    password: str


class ClearEmailsCommand(BaseModel):
    account_id: str

##

class ClearEmailsPayload(BaseModel):
    account_id: str


class CreateMailPremiumPayload(BaseModel):
    account_id: str
    domain_id: int
    email: str
    password: str
    init_at: int
    expire: int


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

class ServiceResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None


class CreateEmailPremiumResponse(ServiceResponse):
    account_id: Optional[str]
    email: Optional[EmailStr]


class MailCreateFreeResponse(ServiceResponse):
    email: Optional[EmailStr]
    expire: Optional[int]


class MailRefillResponse(ServiceResponse):
    email: Optional[EmailStr] = None
    expire: Optional[int] = None


class MailExpireResponse(ServiceResponse):
    remaining: Optional[int] = None


class MailDeletePayload(BaseModel):
    account_id: str
    email: EmailStr


class MailDeleteResponse(ServiceResponse):
    account_id: Optional[str] = None
    email: Optional[EmailStr] = None


class MailCreateQuotaResponse(ServiceResponse):
    account_id: Optional[str] = None
    email_limit: Optional[int] = None
    custom_email_limit: Optional[int] = None
    alias_limit: Optional[int] = None


class MailUpdateQuotaResponse(ServiceResponse):
    account_id: Optional[str] = None
    email_limit: Optional[int] = None
    custom_email_limit: Optional[int] = None
    alias_limit: Optional[int] = None


class DeactivateMailPayload(BaseModel):
    account_id: str
    email: EmailStr


class DeactivateMailResponse(ServiceResponse):
    account_id: Optional[str] = None
    email: Optional[EmailStr] = None


class MailGetQuotaResponse(ServiceResponse):
    account_id: Optional[str] = None
    email_limit: Optional[int] = None
    custom_email_limit: Optional[int] = None
    alias_limit: Optional[int] = None


class GetEmailResponse(ServiceResponse):
    email: Optional[EmailStr] = None
    expire: Optional[int] = None
    active: Optional[int] = None

class GetEmailsResponse(ServiceResponse):
    emails: List[GetEmailResponse]

class ActivateEmailResponse(ServiceResponse):
    email: Optional[EmailStr] = None
    active: Optional[int] = None


class ClearEmailsResponse(ServiceResponse):
    account_id: Optional[str] = None
