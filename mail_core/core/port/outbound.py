from typing import Protocol


class MailCoreRepository(Protocol):

    def get_email(self, payload):
        ...

    def get_encrypt_password(self, payload):
        ...

    def get_free_domain_name(self):
        ...

    def get_premium_domain_name(self):
        ...

    def create_email(self, payload):
        ...

    def get_account_quota(self, payload):
        ...

    def create_quota(self, payload):
        ...

    def update_quota(self, payload):
        ...

    def update_quota_email_limit(self, payload):
        ...

    def get_default_interval(self):
        ...

    def get_expire(self, payload):
        ...

    def set_expire(self, payload):
        ...

    def delete_email(self, payload):
        ...

    def deactivate(self, payload):
        ...

    def activate(self, payload):
        ...

    def get_email_info(self, payload):
        ...

    def get_account_emails(self, payload):
        ...

    def clear_emails(self, payload):
        ...
