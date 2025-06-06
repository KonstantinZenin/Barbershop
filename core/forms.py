
from django import forms
from .models import Review, Master, Service, Order
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


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


class OrderForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['master', 'services', 'client_name', 'phone', 'appointment_date', 'comment']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'client_name': forms.TextInput(attrs={
                'class': 'form-control quantum-input',
                'placeholder': 'Ваше имя'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control quantum-input',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем минимальную дату - сегодня
        self.fields['appointment_date'].widget.attrs['min'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
        
        # Если передан мастер, обновляем список услуг
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['services'].queryset = Service.objects.filter(masters__id=master_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['services'].queryset = self.instance.master.services.all()
            