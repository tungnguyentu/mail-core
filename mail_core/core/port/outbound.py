from typing import Protocol


class MailCoreRepository(Protocol):

    def get_free_domain_name(self) -> list:
        pass

    def get_email(self, email: str) -> str:
        pass

    def get_expire(self, email: str) -> int:
        pass

    def create_email(self, email: str) -> str:
        pass

    def set_expire(self, email: str, expire: int) -> None:
        pass
