from django.urls import path
from .views import (
    MainView,
    CreateView,
)

app_name="unit"

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('create/', CreateView.as_view(), name="create"),
]
