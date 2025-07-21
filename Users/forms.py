from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    """Форма для входа пользователя в систему."""
    def __init__(self, *args, **kwargs):
        """Инициализация формы входа: настройка полей."""
        super().__init__(*args, **kwargs)
        # Кастомизация поля username
        self.fields['username'].label = "Email или имя пользователя"
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Введите email или имя пользователя'
        })
        # Кастомизация поля password
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
        
        # Обновление сообщений об ошибках
        self.error_messages['invalid_login'] = (
            "Пожалуйста, введите правильные email/имя пользователя и пароль."
        )


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'}),
        required=True,
        error_messages={
            'required': 'Обязательное поле',
            'invalid': 'Введите правильный email адрес',
            'unique': 'Пользователь с таким email уже существует'
        }
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Телефон (необязательно)'}),
        required=False,
        max_length=20,
        error_messages={
            'max_length': 'Телефон слишком длинный (макс. 20 символов)'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')
        error_messages = {
            'username': {
                'required': 'Обязательное поле',
                'max_length': 'Слишком длинное имя пользователя',
                'unique': 'Пользователь с таким именем уже существует'
            },
            'email': {
                'unique': 'Пользователь с таким email уже существует'
            },
            'password2': {
                'password_mismatch': 'Пароли не совпадают'
            }
        }
        
    def __init__(self, *args, **kwargs):
        """Инициализация формы входа: настройка полей и сообщений об ошибках."""
        super().__init__(*args, **kwargs)
        
        # Кастомизация поля username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя',
        })
        # Кастомизация поля password1
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Придумайте пароль',
        })
        # Кастомизация поля password2
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        })
        
        # Русификация сообщений об ошибках для паролей
        self.fields['password1'].error_messages = {
            'required': 'Обязательное поле',
            'password_too_short': 'Пароль слишком короткий (мин. 8 символов)',
            'password_common': 'Пароль слишком простой',
            'password_entirely_numeric': 'Пароль не может состоять только из цифр'
        }
        
        # Русификация для поля password2
        self.fields['password2'].error_messages = {
            'password_mismatch': 'Пароли не совпадают'
        }
        
        # Сбрасываем подсказки (help_text) для полей, чтобы не отображались
        for field_name in ('username', 'password1', 'password2'):
            if self.fields.get(field_name):
                self.fields[field_name].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
