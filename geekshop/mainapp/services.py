import random

from mainapp.models import Product


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_prod):
    products_list = Product.objects.filter(category=hot_prod.category).exclude(pk=hot_prod.pk)[:3]
    return products_list
