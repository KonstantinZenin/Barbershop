import re
from django.http import HttpResponse
from django.shortcuts import render
from .data import *


def landing(request):
    context = {
        "title_masters": "Наши мастера",
        "masters": masters,
        "title_services": "Наши услуги",
        "services": services,}
    return render(request, "core/landing.html", context)


def thanks(request):
    context = {}
    return render(request, "core/thanks.html", context)


def orders_list(request):
    context = {
        'title': 'КВАНТОВЫЙ ТРЕКЕР ЗАКАЗОВ',
        'orders': orders,
    }
    return render(request, "core/orders_list.html", context)


def order_detail(request, order_id):
    return HttpResponse(f"Order {order_id}")
