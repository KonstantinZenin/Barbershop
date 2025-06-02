
from django import forms
from .models import Review, Master, Service
from django.core.validators import MinValueValidator, MaxValueValidator


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'is_popular', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }



class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control quantum-input',
                'placeholder': 'Ваше имя'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control quantum-input',
                'placeholder': 'Ваш отзыв...',
                'rows': 4
            }),
            'master': forms.Select(attrs={
                'class': 'form-select quantum-select',
                'id': 'id_master'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control quantum-file-input'
            })
        }
        labels = {
            'client_name': 'Имя клиента',
            'text': 'Текст отзыва',
            'master': 'Мастер',
            'photo': 'Фото (необязательно)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.filter(is_active=True)
