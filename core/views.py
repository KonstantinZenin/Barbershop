from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .forms import *
from django.contrib import messages


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
    # Определяем тип благодарности по параметру URL
    source = request.GET.get('source', 'booking')
    
    context = {
        'countdown_seconds': 15,
        'redirect_url': reverse('landing'),
        'is_review': source == 'review'
    }
    return render(request, "core/thanks.html", context)


@staff_member_required
def orders_list(request):
    # Базовая выборка с оптимизацией запросов
    orders = Order.objects.select_related('master').prefetch_related('services').all()
    
    # Обработка поискового запроса
    search_query = request.GET.get('q', '')
    if search_query:
        # Получаем выбранные поля для поиска
        search_fields = request.GET.getlist('search_in', ['name'])  # По умолчанию имя
        
        # Строим Q-объекты
        filters = Q()
        
        if 'name' in search_fields:
            filters |= Q(client_name__icontains=search_query)
            
        if 'phone' in search_fields:
            filters |= Q(phone__icontains=search_query)
            
        if 'comment' in search_fields:
            filters |= Q(comment__icontains=search_query)

        # Применяем фильтры только если есть выбранные поля
        if filters:
            orders = orders.filter(filters)

    # Сортировка и формирование контекста
    context = {
        'title': 'КВАНТОВЫЙ ТРЕКЕР ЗАКАЗОВ',
        'orders': orders.order_by('-date_created'),
    }
    
    return render(request, "core/orders_list.html", context)


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context = {
        "order": order,
    }

    return render(request, "core/order_detail.html", context)


@staff_member_required
def service_create(request):

    if request.method == "GET":
        form = ServiceForm()
        context = {
        'title': 'Создание квантовой услуги',
        'form': form,
    }

        return render(request, 'core/service_create.html', context)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Услуга {form.cleaned_data["name"]} успешно создана!')
                return redirect("landing")
            except ValidationError as e:
                form.add_error(None, e)
    
        context = {
            'title': 'Создание квантовой услуги',
            'form': form,
        }
        
        return render(request, 'core/service_create.html', context)
    
    
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = False
            review.save()
            # Добавляем параметр source=review
            return redirect(f"{reverse('thanks')}?source=review")
    else:
        form = ReviewForm()
    
    context = {
        'title': 'Квантовый отзыв',
        'form': form
    }
    return render(request, 'core/review_form.html', context)


def get_master_info(request):
    """AJAX-представление для получения информации о мастере"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                master_data = {
                    'id': master.id,
                    'name': f"{master.first_name} {master.last_name}",
                    'experience': master.experience,
                    'photo': master.photo.url if master.photo else None,
                    'services': [{'name': service.name} for service in master.services.all()],
                }
                return JsonResponse({'success': True, 'master': master_data})
            except Master.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Мастер не найден'})
        return JsonResponse({'success': False, 'error': 'Не указан ID мастера'})
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос'})
