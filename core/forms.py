from django import forms
from django.core.exceptions import ValidationError
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'is_popular', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }