from .models import Order, Review
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
# Импорт всего что нужно для работы бота
from .telegram_bot import send_telegram_message
from asyncio import run
# Из настроек импортируем токен и id чата
from django.conf import settings
from django.urls import reverse
from.mistral import is_bad_review

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID

@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """
    Проверяет текст отзыва по заданным в настройках градациям
    """
    if created:
        if not is_bad_review(instance.text):
            instance.is_published = True
            instance.save()
            # Отправка в телеграм
            message = f"""
*Новый отзыв от клиента*
*Имя:* {instance.client_name}
*Текст:* {instance.text}
*Оценка:* {instance.rating}
*Ссылка на отзыв:* http://127.0.0.1:8000/admin/core/review/{instance.id}/change/

#отзыв
"""
            run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))
        
        
        else:
            instance.is_published = False
            instance.save()
            # Вывод в терминал 
            print(f"Отзыв '{instance.client_name}' не опубликован из-за негативных слов.")



@receiver(m2m_changed, sender=Order.services.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на консультацию.
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        # Получаем список услуг
        services = [f"✨ {service.name}" for service in instance.services.all()]

        # Форматирование даты и времени
        appointment_date = instance.appointment_date.strftime("%d.%m.%Y %H:%M") if instance.appointment_date else 'не указана'
        date_created = instance.date_created.strftime("%d.%m.%Y %H:%M")

        # Создаем динамическую ссылку на админку с fallback
        try:
            admin_path = reverse('admin:core_order_change', args=[instance.id])
            admin_url = f"{settings.BASE_URL}{admin_path}" if hasattr(settings, 'BASE_URL') else f"http://127.0.0.1:8000{admin_path}"
        except:
            admin_url = f"http://127.0.0.1:8000/admin/core/order/{instance.id}/change/"

        # Формируем сообщение
        message = f"""
⚡ *КВАНТОВОЕ УВЕДОМЛЕНИЕ: НОВАЯ ЗАПИСЬ* ⚡

🔹 *Клиент:* `{instance.client_name}`
📞 *Телефон:* `{instance.phone or 'не указан'}`
💬 *Комментарий:* `{instance.comment or 'не указан'}`

🛠 *Услуги:*
{chr(10).join(services) or 'не указаны'}

⏳ *Дата создания:* `{date_created}`
👨‍🎨 *Мастер:* `{instance.master.first_name} {instance.master.last_name}`
📅 *Дата записи:* `{appointment_date}`

🔗 *Ссылка на админку:* 
{admin_url}

#запись #{instance.master.last_name.lower()}
-------------------------------------------------------------
        """
        run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))