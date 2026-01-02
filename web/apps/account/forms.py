from django import forms
from .models import (
    Profile,
    Status,
)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["message", "foto"]
        widgets = {
            "message": forms.Textarea(attrs={
                "placeholder": "what do you think...",
                "class": "form-control"
            }),
        }