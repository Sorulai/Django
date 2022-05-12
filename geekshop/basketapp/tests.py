from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from mainapp.models import Product, ProductCategory


class BasketTestCase(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                name=f'prod{i}',
                category=self.category,
                short_desc='shortdesc',
                description='desc'
            )
        self.client = Client()

    def test_redirect(self):
        product = Product.objects.first()
        response = self.client.get(f'/basket/add/{product.pk}/')
        self.assertEqual(response.status_code, self.status_redirect)