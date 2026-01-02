from django.db import models
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from apps.unit.models import Unit

# Create your models here.
class MonthlyMessageCounter(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()
    last_number = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('year', 'month')
        
def get_next_message_id():
    now = timezone.now()
    year = now.year
    month = now.month

    with transaction.atomic():
        counter, _ = MonthlyMessageCounter.objects.select_for_update().get_or_create(
            year=year,
            month=month,
            defaults={'last_number': 0}
        )

        counter.last_number += 1
        counter.save(update_fields=['last_number'])

        return counter.last_number, year, month

    
class HaulingCheckRecord(models.Model):
    LOAD_CHOICES = [
        ("1", "Coal"),
        ("2", "Over Burden"),
        ("3", "Etc"),
        ("4", "No Load"),
    ]
    
    STATUS_CHOICES = [
        ("1", "IN"),
        ("2", "OUT"),
    ]
    
    id_message = models.PositiveIntegerField(editable=False)
    message_year = models.PositiveIntegerField(editable=False)
    message_month = models.PositiveSmallIntegerField(editable=False)
    
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    load = models.CharField(max_length=50, choices=LOAD_CHOICES, default=LOAD_CHOICES[0][0])
    message = models.TextField()

    checker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        if self._state.adding:  # CREATE saja
            number, year, month = get_next_message_id()
            self.id_message = number
            self.message_year = year
            self.message_month = month
        
        super().save(*args, **kwargs)