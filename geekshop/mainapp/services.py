import json
import random

from django.conf import settings

from mainapp.models import Product
import requests


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_prod):
    products_list = Product.objects.filter(category=hot_prod.category).exclude(pk=hot_prod.pk).select_related()[:3]
    return products_list



