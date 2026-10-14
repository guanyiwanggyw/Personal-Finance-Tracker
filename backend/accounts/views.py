from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountListSerializer, AccountSerializer


class AccountListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Account.objects.filter(owner=self.request.user)
            .exclude(type=Account.AccountType.EXTERNAL)
            .select_related("bankaccount")
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AccountListSerializer
        return AccountSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AccountDelete(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(
            owner=self.request.user,
        ).exclude(type=Account.AccountType.EXTERNAL)