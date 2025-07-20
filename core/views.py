from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views import View
from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin  # Добавляем импорт


class StaffRequiredMixin:
    """Миксин для проверки прав staff"""
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LandingView(TemplateView):
    template_name = "core/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title_masters": "Наши мастера",
            "masters": Master.objects.prefetch_related('services').filter(is_active=True),
            "title_services": "Наши услуги",
            "services": Service.objects.all(),
            "reviews": Review.objects.filter(is_published=True).select_related('master')[:6]
        })
        return context


class ThanksView(TemplateView):
    template_name = "core/thanks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source = self.request.GET.get('source', 'booking')
        context.update({
            'countdown_seconds': 15,
            'redirect_url': reverse('landing'),
            'is_review': source == 'review'
        })
        return context


class OrdersListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "core/orders_list.html"
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('master').prefetch_related('services')
        
        search_query = self.request.GET.get('q', '')
        if search_query:
            search_fields = self.request.GET.getlist('search_in', ['name'])
            filters = Q()
            
            if 'name' in search_fields:
                filters |= Q(client_name__icontains=search_query)
            if 'phone' in search_fields:
                filters |= Q(phone__icontains=search_query)
            if 'comment' in search_fields:
                filters |= Q(comment__icontains=search_query)
            
            if filters:
                queryset = queryset.filter(filters)
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КВАНТОВЫЙ ТРЕКЕР ЗАКАЗОВ'
        
        # Получаем список выбранных полей для поиска
        selected_search_fields = self.request.GET.getlist('search_in', [])
        # Если нет выбранных полей (первый заход), устанавливаем только 'name'
        if not selected_search_fields:
            selected_search_fields = ['name']
        
        context['selected_search_fields'] = selected_search_fields
        return context


class OrderDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Order
    template_name = "core/order_detail.html"
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'


class ServiceCreateView(StaffRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание квантовой услуги'
        return context

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Услуга {form.cleaned_data["name"]} успешно создана!')
            return response
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
    
class MasterDetailView(DetailView):
    model = Master
    template_name = 'core/master_detail.html'
    context_object_name = 'master'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('services', 'review_set')

    def get_object(self, queryset=None):
        try:
            master = super().get_object(queryset)
        except Master.DoesNotExist:
            # Обработка 404 для несуществующих мастеров
            return redirect('landing')  # Перенаправление на главную
            
        # Сохраняем просмотренного мастера в сессии
        viewed_masters = self.request.session.get('viewed_masters', [])
        if master.id not in viewed_masters:
            viewed_masters.append(master.id)
            self.request.session['viewed_masters'] = viewed_masters
            
            # Увеличиваем счетчик только один раз за сессию
            Master.objects.filter(pk=master.pk).update(view_count=models.F('view_count') + 1)
            master.refresh_from_db()
        
        return master

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'КВАНТОВЫЙ МАСТЕР: {self.object.first_name} {self.object.last_name}'
        context['master'] = self.object  # Явно передаём объект мастера
        return context

class ServicesListView(StaffRequiredMixin, ListView):
    model = Service
    template_name = 'core/services_list.html'
    context_object_name = 'services'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КВАНТОВЫЙ КАТАЛОГ УСЛУГ'
        return context

class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_update.html'
    success_url = reverse_lazy('services_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'РЕДАКТИРОВАНИЕ УСЛУГИ: {self.object.name}'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Услуга "{self.object.name}" успешно обновлена!')
        return response
    
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'

    def get_initial(self):
        initial = super().get_initial()
        master_id = self.request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                initial['master'] = master
            except Master.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Квантовый отзыв'
        
        # Передаем ID мастера в контекст для отображения в шаблоне
        master_id = self.request.GET.get('master_id')
        if master_id:
            context['selected_master_id'] = master_id
            
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        review.is_published = False
        review.save()
        return redirect(f"{reverse('thanks')}?source=review")


class GetMasterInfoView(View):
    def get(self, request):
        # Строгая проверка заголовков
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Недопустимый запрос'}, status=400)
            
        master_id = request.GET.get('master_id')
        if not master_id:
            return JsonResponse({'success': False, 'error': 'Не указан ID мастера'}, status=400)
            
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
            return JsonResponse({'success': False, 'error': 'Мастер не найден'}, status=404)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Квантовая запись'
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.status = 'not_approved'
        order.save()
        form.save_m2m()
        messages.success(self.request, 'Ваша запись успешно создана!')
        return redirect(f"{reverse('thanks')}?source=booking")


class GetServicesByMasterView(View):
    def get(self, request):
        # Строгая проверка заголовков
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Недопустимый запрос'}, status=400)
            
        master_id = request.GET.get('master_id')
        if not master_id:
            return JsonResponse({'success': False, 'error': 'Не указан ID мастера'}, status=400)
            
        try:
            master = Master.objects.get(pk=master_id)
            services = master.services.all().values('id', 'name')
            return JsonResponse({'success': True, 'services': list(services)})
        except Master.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Мастер не найден'}, status=404)
