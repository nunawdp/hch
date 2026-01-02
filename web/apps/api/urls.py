from django.urls import path
from apps.api.views.unit import (
    APIUnitList,
)


app_name="api"

urlpatterns = [
    path('unit/', APIUnitList.as_view(), name="API-unit-list")
]
