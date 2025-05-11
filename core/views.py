from django.http import HttpResponse
from django.shortcuts import render
from .data import *
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import *


def landing(request):
    context = {
        "title_masters": "Наши мастера",
        "masters": Master.objects.prefetch_related('services').filter(is_active=True),
        "title_services": "Наши услуги",
        "services": Service.objects.all(),
        "reviews": Review.objects.filter(is_published=True).select_related('master')[:6]
    }
    return render(request, "core/landing.html", context)


def thanks(request):
    context = {
        'countdown_seconds': 15,  # Время отсчета
        'redirect_url': reverse('landing')
    }
    return render(request, "core/thanks.html", context)


@staff_member_required
def orders_list(request):
    context = {
        'title': 'КВАНТОВЫЙ ТРЕКЕР ЗАКАЗОВ',
        'orders': orders,
    }
    return render(request, "core/orders_list.html", context)


@staff_member_required
def order_detail(request, order_id):
    try:
        order = [o for o in orders if o["id"] == order_id][0]
    except IndexError:
        return HttpResponse(status=404)

    context = {
        "order": order,
    }

    return render(request, "core/order_detail.html", context)
