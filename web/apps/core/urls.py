from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomeView,
    DashboardView,
    LoginView,
    LogoutSuccessView,
)

app_name='core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="core:logout-success"), name='logout'),
    path('logout/success/', LogoutSuccessView.as_view(), name='logout-success'),
]