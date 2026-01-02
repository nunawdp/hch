from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.views.generic import (
    View,
    TemplateView,
    DetailView,
    ListView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from apps.account.models import Status, Profile


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"
    

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    
    def get_context_data(self, **kwargs):
        status_feed = Status.objects.all().order_by("-created")
        total_feed = len(status_feed)
        
        context = {
            "status_feed": status_feed[:5],
            "total_feed": total_feed,
        }
        self.kwargs.update(context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)
    
class LoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = AuthenticationForm
    
    # cegah user yang sudah login untuk tidak dapat akses halaman login
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)
    
    # periksa apakah username & password cocok dengan database
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("invalid")
            return self.form_invalid(form)
    
    # redirect ke home jika login sukses
    def get_success_url(self):
        return reverse_lazy("core:home")


class LogoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "core/logout.html"