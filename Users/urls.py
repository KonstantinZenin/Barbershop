from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='registerUser'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='users/password_change.html',
        success_url=reverse_lazy('users:profile')
    ), name='password_change'),
]
