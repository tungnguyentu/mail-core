from pydantic import BaseModel


class CreateFreeEmailDTO(BaseModel):
    account_id: str


class RefillDTO(BaseModel):
    email: str


class GetExpireDTO(BaseModel):
    account_id: str
    email: str
