from email.mime import image
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


class Master(models.Model):

    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images/masters/", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    adress = models.CharField(max_length=255, verbose_name="Адрес")
    experiece = models.PositiveBigIntegerField(verbose_name="Стаж", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ["first_name", "last_name"]


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="images/services/", blank=True, null=True, verbose_name="Изображение услуги")

    def __str__(self):
        return f'{self.name} - {self.price} руб.'
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]
