from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    TemplateView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User
from .models import Status
from .forms import (
    StatusForm,
)


# Create your views here.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        all_status = user.status.filter(user=user)
        last_status = all_status.order_by("-created").first()
        
        context = {
            "page_title" : "Profile",
            "last_status": last_status
        }
        return render(request, 'account/profile.html', context)

class StatusCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("foto")
        if file and file.size > 10 * 1024 * 1024:
            return JsonResponse({"message": "Limited file size reached"}, status=400)

        form = StatusForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("account:profile")
        else:
            return JsonResponse({"message": "failed"}, status=500)