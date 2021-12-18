from django.db import models

# Create your models here.
from authapp.models import ShopUser
from mainapp.models import Product


class FavoritesProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, verbose_name='Пользователь')