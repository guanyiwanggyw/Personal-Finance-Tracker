from django.conf import settings
from django.db import models
from django.utils import timezone
from django_cryptography.fields import encrypt


class ProviderConnection(models.Model):
    class Provider(models.TextChoices):
        MONZO = "monzo"
        # add more banks later

    class Status(models.TextChoices):
        CONNECTED = "connected"
        NEEDS_REAUTH = "needs_reauth"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_connections",
    )
    provider = models.CharField(max_length=20, choices=Provider.choices)
    access_token = encrypt(models.TextField(blank=True))
    refresh_token = encrypt(models.TextField(blank=True))
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONNECTED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "provider"],
                name="uniq_provider_connection_per_owner",
            ),
        ]

    def __str__(self):
        return f"{self.get_provider_display()} ({self.status})"

class Account(models.Model):
    class AccountType(models.TextChoices):
        CASH = "cash"
        BANK = "bank"
        EXTERNAL = "external"  # shops, workplaces, etc.

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="accounts",
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=AccountType.choices)
    currency = models.CharField(max_length=3, default="GBP")
    is_closed = models.BooleanField(default=False)
    opened_at = models.DateTimeField(default=timezone.now)
    balance_minor_unit = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="uniq_account_name_per_owner"
            ),
        ]

    def __str__(self):
        return self.name

    def balance_minor_units(self):
        # shared logic: sum this account's transactions
        ...


class BankAccount(Account):
    connection = models.ForeignKey(
        ProviderConnection,
        on_delete=models.PROTECT,
        related_name="bank_accounts",
    )
    external_id = models.CharField(max_length=100)  # e.g. Monzo acc_...
    account_number = models.CharField(max_length=20, blank=True)
    sort_code = models.CharField(max_length=8, blank=True)
    provider_balance_minor_units = models.BigIntegerField(null=True, blank=True)
    balance_as_of = models.DateTimeField(null=True, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["connection", "external_id"],
                name="uniq_external_id_per_connection",
            ),
        ]

    def save(self, *args, **kwargs):
        self.type = Account.AccountType.BANK
        super().save(*args, **kwargs)

    def sync(self):
        # only bank accounts can sync, so this method lives here
        ...