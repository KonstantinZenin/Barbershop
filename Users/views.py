from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView as BasePasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserProfileUpdateForm, UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
# Импорт служебных вью для сброса и восстановления пароля
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

class ProfileView(LoginRequiredMixin, TemplateView):
    """Представление личного кабинета пользователя"""
    template_name = "users/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['password_change_form'] = UserPasswordChangeForm(user=user)
        context['profile_form'] = UserProfileUpdateForm(instance=user)
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""
    model = User
    form_class = UserProfileUpdateForm
    template_name = "users/profile_update_form.html"
    success_url = reverse_lazy("users:profile")
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class UserPasswordChangeView(LoginRequiredMixin, BasePasswordChangeView):
    """Представление для смены пароля пользователя."""
    form_class = UserPasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:profile")
    
    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)


class CustomPasswordResetView(PasswordResetView):
    """Кастомное представление для запроса сброса пароля."""
    form_class = CustomPasswordResetForm
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Кастомное представление после отправки запроса на сброс пароля."""
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Кастомное представление для ввода нового пароля."""
    form_class = CustomSetPasswordForm
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Кастомное представление об успешном сбросе пароля."""
    template_name = "users/password_reset_complete.html"

class UserRegisterView(CreateView):
    """
    Представление для регистрации новых пользователей.
    """

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("landing")

    def dispatch(self, request, *args, **kwargs):
        """Перенаправляет аутентифицированных пользователей на главную страницу."""
        if request.user.is_authenticated:
            return redirect("landing")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Обрабатывает валидную форму: сохраняет пользователя и выполняет вход"""
        user = form.save()
        # Автоматическая аутентификация с указанием бэкенда
        from django.contrib.auth import login
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(
            self.request,
            f"Добро пожаловать, {user.username}! Регистрация прошла успешно.",
        )
        return redirect('landing')

    def form_invalid(self, form):
        """Обрабатывает невалидную форму: выводит сообщение об ошибке."""
        messages.error(
            self.request, "Пожалуйста, исправьте ошибки в форме регистрации."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавляет заголовок страницы в контекст."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация"
        return context


class UserLoginView(LoginView):
    """Представление для аутентификации пользователей."""

    template_name = "users/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """Определяет URL для перенаправления после успешного входа."""
        messages.success(self.request, f"С возвращением, {self.request.user.username}!")
        next_url = self.request.GET.get("next")
        return next_url or reverse_lazy("landing")

    def form_invalid(self, form):
        """Обрабатывает невалидную форму: выводит сообщение об ошибке."""
        messages.error(
            self.request, "Неверное имя пользователя или пароль. Попробуйте снова."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавляет заголовок страницы в контекст."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        return context


class UserLogoutView(LogoutView):
    """Представление для выхода пользователей из системы."""

    next_page = reverse_lazy("landing")

    def dispatch(self, request, *args, **kwargs):
        """Добавляет сообщение об успешном выходе для аутентифицированных пользователей."""
        if request.user.is_authenticated:
            messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)
