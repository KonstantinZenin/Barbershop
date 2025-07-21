from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameAuthBackend(ModelBackend):
    """Кастомный бэкенд для аутентификации по email или username"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None or password is None:
            return None
        
        try:
            # Пробуем найти пользователя по email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                # Если по email не найден, пробуем по username
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Возвращаем None если пользователь не найден
                return None
        except UserModel.MultipleObjectsReturned:
            # Если найдено несколько пользователей с одинаковым email
            return None
        
        # Проверяем пароль и возвращаем пользователя
        if user.check_password(password):
            return user
        
        return None
