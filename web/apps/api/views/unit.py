from django.shortcuts import render
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http.response import JsonResponse
from apps.unit.models import Unit
from django.views.generic import View
from apps.api.serializers.unit import unit_serializer


class APIUnitList(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q','')
        qs = Unit.objects.annotate(
            combined=Concat('prefix', 'code')
        ).filter(
            Q(name__icontains=q) |
            Q(prefix__icontains=q) |
            Q(code__icontains=q) |
            Q(combined__icontains=q)
        ).order_by('code')[:4]

        data = [
            unit_serializer(obj)
            for obj in qs
        ]
        return JsonResponse(data, safe=False)

