from django.urls import path
from .views import (
    ProfileView,
    StatusCreateView,
)


app_name="account"

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="profile"),
    path('status/create', StatusCreateView.as_view(), name="create-status")
]
