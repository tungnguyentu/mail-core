from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    init_at: int
    expire: int


class Domain(BaseModel):
    name: str
    domain_id: int


class MailCreatePayload(BaseModel):
    email: EmailStr
    password: str
    domain_id: str
    init_at: int
    expire: int


class MailCreateResponse(BaseModel):
    email: EmailStr
    expire: int
