from django.test import TestCase
from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(
            name='cat1'
        )
        # for i in range(10):
        #     Product.objects.create(
        #         name=f'prod{i}',
        #         category=self.category,
        #         short_desc='shortdesc',
        #         description='desc'
        #     )
        self.product_1 = Product.objects.create(name="стул 1",
                                                category=self.category,
                                                price=1999.5,
                                                quantity=150,
                                                short_desc='short_desc',
                                                description='desc'
                                                )

        self.product_2 = Product.objects.create(name="стул 2",
                                                category=self.category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False,
                                                short_desc='short_desc',
                                                description='desc'
                                                )

    def test_product_get(self):
        prod1 = Product.objects.get(name="стул 1")
        prod2 = Product.objects.get(name="стул 2")
        self.assertEqual(prod1, self.product_1)
        self.assertEqual(prod2, self.product_2)

