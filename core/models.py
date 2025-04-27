import re
from django import db
from django.db import models


class Order(models.Model):

    STATUS_CHOICES = [
        ("not_approved", "Не подтвержден"),
        ("moderated", "Прошел модерацию"),
        ("spam", "Спам"),
        ("approved", "Подтвержден"),
        ("in_awaiting", "В ожидании"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    status = models.CharField(max_length=50, verbose_name="Статус", choices=STATUS_CHOICES, default="not_approved")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    date_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name='orders')
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ №{self.id} от {self.client_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]