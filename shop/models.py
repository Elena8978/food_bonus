from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class Client(AbstractUser):
    bonus_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Баланс бонусов"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    image = models.ImageField(upload_to='dishes/', verbose_name="Фото", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Order(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Заказанное блюдо"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Заказавший клиент"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ {self.id} — {self.dish.name} ({self.client.username})"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']