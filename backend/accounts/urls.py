from django.urls import path
from . import views

urlpatterns = [
    path("", views.AccountListCreate.as_view(), name="account-list-create"),
    path("<int:pk>/", views.AccountDelete.as_view(), name="account-delete"),
]
