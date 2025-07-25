from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Order(models.Model):
    """Модель заказа."""

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
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name='orders')
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ №{self.id} от {self.client_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]
        indexes = [
            # Одиночные  Индексы по имени клиента, номеру телефона и комментарию
            models.Index(fields=["client_name"], name="order_client_name_idx"),
            models.Index(fields=["phone"], name="phone_idx"),
            models.Index(fields=["comment"], name="comment_idx"),
            # Составной индекс по имени клиента и номеру телефона
            models.Index(fields=["client_name", "phone"], name="client_name_phone_idx"),
            # Составной индекс по имени клиента и комментарию
            models.Index(fields=["client_name", "comment"], name="client_name_comment_idx"),
        ]


class Master(models.Model):
    """Модель мастера."""

    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="images/masters/", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveBigIntegerField(verbose_name="Стаж", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ["first_name", "last_name"]
        indexes = [
            # Индек по имени
            models.Index(fields=["first_name"], name="first_name_idx"),
        ]


class Service(models.Model):
    """Модель услуги."""

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
        indexes = [
            # Индекс по названию
            models.Index(fields=["name"], name="name_idx"),            
        ]


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента", blank=True)
    master = models.ForeignKey("Master", on_delete=models.CASCADE, verbose_name="Мастер")
    photo = models.ImageField(upload_to="images/reviews/", blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField(default=5,
            validators=[
                MinValueValidator(1, message="Рейтинг не может быть меньше 1."),
                MaxValueValidator(5, message="Рейтинг не может быть больше 5.")
            ],
            help_text="Рейтинг от 1 до 5", verbose_name="Оценка")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")


    def __str__(self):
        return f"Отзыв от {self.client_name} на {self.master}"


    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        indexes = [
            # Индекс по имени клиента
            models.Index(fields=["client_name"], name="review_client_name_idx"),
        ]
