from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='registerUser'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]