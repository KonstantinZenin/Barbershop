from django.contrib import admin
from django.urls import path
import core.views as views

urlpatterns = [
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path("service_create/", views.ServiceCreateView.as_view(), name="service_create"),
    path('review/create/', views.ReviewCreateView.as_view(), name='create_review'),
    path('api/master-info/', views.GetMasterInfoView.as_view(), name='get_master_info'),
    path('order/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('api/master-services/', views.GetServicesByMasterView.as_view(), name='get_services_by_master'),
    # Новые пути для HW46
    path('masters/<int:pk>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('services/', views.ServicesListView.as_view(), name='services_list'),
    path('services/update/<int:pk>/', views.ServiceUpdateView.as_view(), name='service_update'),
]
