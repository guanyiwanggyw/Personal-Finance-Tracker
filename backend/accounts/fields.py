from cryptography.fernet import Fernet, InvalidToken, MultiFernet
from django.conf import settings
from django.db import models


def _fernet():
    # encrypts with the first key, decrypts with any of them
    return MultiFernet([Fernet(k) for k in settings.FIELD_ENCRYPTION_KEYS])


class EncryptedTextField(models.TextField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return value
        return _fernet().encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        try:
            return _fernet().decrypt(value.encode()).decode()
        except InvalidToken:
            raise ValueError("Cannot decrypt token: wrong or missing FIELD_ENCRYPTION_KEYS")