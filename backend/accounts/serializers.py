from rest_framework import serializers

from .models import Account, BankAccount


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "owner",
            "name",
            "type",
            "currency",
            "is_closed",
            "opened_at",
            "balance_minor_unit",
        ]
        read_only_fields = [
            "id",
            "owner",
            "opened_at",
            "balance_minor_unit",
        ]

    def validate_type(self, value):
        if value == Account.AccountType.BANK:
            raise serializers.ValidationError(
                "Bank accounts are created by connecting a bank provider."
            )
        return value


class BankAccountSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = BankAccount
        fields = AccountSerializer.Meta.fields + [
            "connection",
            "external_id",
            "account_number",
            "sort_code",
            "provider_balance_minor_units",
            "balance_as_of",
            "last_synced_at",
        ]
        read_only_fields = fields


class AccountListSerializer(AccountSerializer):
    def to_representation(self, instance):
        if instance.type == Account.AccountType.BANK:
            try:
                bank_account = instance.bankaccount
            except BankAccount.DoesNotExist:
                return super().to_representation(instance)
            return BankAccountSerializer(
                bank_account,
                context=self.context,
            ).data

        return super().to_representation(instance)