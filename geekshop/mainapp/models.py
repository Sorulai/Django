import decimal

from django.db import models
# Create your models here.
from model_utils import FieldTracker

from authapp.models import ShopUser
from mainapp.service_currency import get_currency


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категория'
        ordering = ('-id',)

    def delete(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Картинка')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    count_sales = models.PositiveIntegerField(default=0, verbose_name='Количество покупок')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category})'

    def delete(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

    def add_count_sales(self, count):
        self.count_sales += count
        self.save()

    @property
    def price_in_currency(self):
        usd = get_currency()
        usd_price = self.price / decimal.Decimal(usd)
        return round(usd_price, 3)



