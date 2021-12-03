from django.conf import settings
from django.db import models

# Create your models here.
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    add_datetime = models.DateField(auto_now_add=True)

    @property
    def products_cost(self):
        return self.quantity * self.product.price

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.products_cost, _items)))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
