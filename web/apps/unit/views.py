from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic import (
    View,
    TemplateView,
)
from .models import (
    Unit
)

# Create your views here.
class MainView(TemplateView):
    template_name = "unit/main.html"
    
    def get_context_data(self, **kwargs):
        unit = Unit.objects.all()
        context = {
            "unit" : unit
        }
        self.kwargs.update(context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)


class CreateView(View):
    template_name = 'unit/create.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        self.kwargs.update(context)
        kwargs = self.kwargs
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return JsonResponse({'status': 'success'})