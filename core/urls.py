from django.contrib import admin
from django.urls import path
from django.views import View
import core.views as views

urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail,name='order_detail'),
    path("service_create/", views.service_create, name="service_create"),
    path('review/create/', views.create_review, name='create_review'),
]
