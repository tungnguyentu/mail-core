from typing import Protocol
from mail_core.models.mail import MailCreateResponse


class MailUseCase(Protocol):
    
    def create_random_email_address(self, command):
        ...
    
    def refill(self, command):
        ...
    
    def get_time_remaining(self, command):
        ...
    
    def deactivate_email(self, command):
        ...
    
    def activate_email(self, command):
        ...
    
    def delete_email(self, command):
        ...
    
    def create_account_quota(self, command):
        ...
    
    def update_account_quota(self, command):
        ...

