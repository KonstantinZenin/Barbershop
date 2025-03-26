from django.contrib import admin
from django.urls import path
import core.views as views

urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
