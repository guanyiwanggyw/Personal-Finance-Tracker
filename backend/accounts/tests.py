from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Account, BankAccount, ProviderConnection


class AccountModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="owner")

    def test_manual_account_stores_owner_and_account_details(self):
        account = Account.objects.create(
            owner=self.user,
            name="Wallet",
            type=Account.AccountType.CASH,
            currency="GBP",
        )

        self.assertEqual(account.owner, self.user)
        self.assertEqual(account.type, Account.AccountType.CASH)
        self.assertEqual(account.currency, "GBP")
        self.assertEqual(account.balance_minor_unit, 0)
        self.assertFalse(account.is_closed)

    def test_account_name_must_be_unique_per_owner(self):
        Account.objects.create(
            owner=self.user,
            name="Wallet",
            type=Account.AccountType.CASH,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Account.objects.create(
                owner=self.user,
                name="Wallet",
                type=Account.AccountType.CASH,
            )

    def test_different_owners_can_use_the_same_account_name(self):
        other_user = get_user_model().objects.create_user(username="other")
        Account.objects.create(
            owner=self.user,
            name="Wallet",
            type=Account.AccountType.CASH,
        )

        account = Account.objects.create(
            owner=other_user,
            name="Wallet",
            type=Account.AccountType.CASH,
        )

        self.assertEqual(account.owner, other_user)


class BankAccountModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="bank-owner")
        self.connection = ProviderConnection.objects.create(
            owner=self.user,
            provider=ProviderConnection.Provider.MONZO,
        )

    def test_bank_account_is_saved_as_bank_and_inherits_account_fields(self):
        bank_account = BankAccount.objects.create(
            owner=self.user,
            connection=self.connection,
            name="Monzo current",
            type=Account.AccountType.CASH,
            external_id="monzo-account-1",
        )

        bank_account.refresh_from_db()
        self.assertEqual(bank_account.type, Account.AccountType.BANK)
        self.assertEqual(bank_account.owner, self.user)
        self.assertEqual(bank_account.connection, self.connection)
        self.assertEqual(bank_account.external_id, "monzo-account-1")

    def test_provider_external_account_id_must_be_unique_per_connection(self):
        BankAccount.objects.create(
            owner=self.user,
            connection=self.connection,
            name="Monzo current",
            type=Account.AccountType.BANK,
            external_id="monzo-account-1",
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            BankAccount.objects.create(
                owner=self.user,
                connection=self.connection,
                name="Monzo duplicate",
                type=Account.AccountType.BANK,
                external_id="monzo-account-1",
            )


class ProviderConnectionModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="connection-owner")

    def test_connection_defaults_to_connected(self):
        connection = ProviderConnection.objects.create(
            owner=self.user,
            provider=ProviderConnection.Provider.MONZO,
        )

        self.assertEqual(
            connection.status,
            ProviderConnection.Status.CONNECTED,
        )

    def test_user_can_have_only_one_connection_per_provider(self):
        ProviderConnection.objects.create(
            owner=self.user,
            provider=ProviderConnection.Provider.MONZO,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            ProviderConnection.objects.create(
                owner=self.user,
                provider=ProviderConnection.Provider.MONZO,
            )