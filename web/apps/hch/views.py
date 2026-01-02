from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import (
    View,
    TemplateView,
)
from .models import (
    HaulingCheckRecord,
)
from apps.unit.models import Unit


# Create your views here.
class MainView(TemplateView):
    template_name = "hch/main.html"
    extra_context = {
        "page_title": "Hauling Check"
    }

    def get_context_data(self, **kwargs):
        # Ambil context awal dari parent class
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['record_list'] = HaulingCheckRecord.objects.order_by('-created')[:5]

        stats = HaulingCheckRecord.objects.aggregate(
                # --- Totalisator All Time ---
                total_record=Count('id', filter=Q(status=2)), # Total Status 2 (All Time)
                total_all_record=Count('id'),                 # Total Semua Data (All Time)
                
                # --- Statistik Hari Ini (Today) ---
                today_co=Count('id', filter=Q(status=2, created__date=today)),
                today_ci=Count('id', filter=Q(status=1, created__date=today)),
                
                load_coal=Count('id', filter=Q(load=1, created__date=today)),
                load_ob=Count('id', filter=Q(load=2, created__date=today)),
                load_etc=Count('id', filter=Q(load=3, created__date=today)),
                load_noload=Count('id', filter=Q(load=4, created__date=today)),
            )
        
        # Base queryset agar lebih efisien
        all_records = HaulingCheckRecord.objects.all()
        
        # Update context dengan data tambahan
        context.update(stats)
        return context


class CreateRecord(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        return render(request, "hch/create.html")

    def post(self, request, *args, **kwargs):
        data = request.POST
        unit = Unit.objects.get(id=data.get('unit'))
        status = data.get('status')
        load = data.get('load')
        message = data.get('message')
        checker = request.user
        
        obj = HaulingCheckRecord(
            unit=unit,
            status=status,
            load=load,
            message=message,
            checker=checker
        )
        if obj.load:
            load = obj.get_load_display()
        new_message = f'{unit.prefix}-{unit.code} passed the checker point with load: {load}.'
        obj.message = new_message
        obj.save()
        return JsonResponse({"status" : "Success"})

class RecordListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "hch/list.html")