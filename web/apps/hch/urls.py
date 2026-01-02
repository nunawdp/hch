from django.urls import path
from .views import (
    RecordListView,
    MainView,
    CreateRecord,
)

app_name="hch"

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('list/', RecordListView.as_view(), name="list"),
    path('add/', CreateRecord.as_view(), name="create")
]
