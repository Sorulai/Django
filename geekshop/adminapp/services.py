from mainapp.models import Product
from ordersapp.models import OrderItem


def add_count_sales_product(obj):
    if obj.status == 'PD':
        orderitems_list = OrderItem.objects.filter(order__pk=obj.pk).select_related().values()
        for item in orderitems_list:
            if Product.objects.get(pk=int(item['product_id'])):
                Product.objects.get(pk=item['product_id']).add_count_sales(item['quantity'])