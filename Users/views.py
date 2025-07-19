from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import redirect, render, get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# Импорт служебных вью для сброса и восстановления пароля
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView

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
        """Обрабатывает валидную форму: сохраняет пользователя и выполняет автоматический вход."""
        response = super().form_valid(form)
        user = form.save()  # Получаем сохраненного пользователя из формы
        login(self.request, user)
        messages.success(
            self.request,
            f"Добро пожаловать, {user.username}! Регистрация прошла успешно.",
        )
        return response

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