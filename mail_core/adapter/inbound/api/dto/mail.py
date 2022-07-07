from pydantic import BaseModel, EmailStr


class CreateFreeEmailDTO(BaseModel):
    account_id: str


class ClearEmailsDTO(BaseModel):
    account_id: str


class CreatePremiumEmailDTO(BaseModel):
    account_id: str
    username: str
    password: str


class RefillDTO(BaseModel):
    email: str
    account_id: str


class GetExpireDTO(BaseModel):
    account_id: str
    email: str


class GetQuotaDTO(BaseModel):
    account_id: str


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


class GetEmailsDTO(BaseModel):
    account_id: str


class GetEmailDTO(BaseModel):
    account_id: str
    email: EmailStr


class DeactivateEmailDTO(BaseModel):
    account_id: str
    email: EmailStr


class ActivateEmailDTO(BaseModel):
    account_id: str
    email: EmailStr
