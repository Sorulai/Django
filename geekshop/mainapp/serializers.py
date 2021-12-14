from rest_framework import serializers

from mainapp.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'category',
            'name',
            'image',
            'short_desc',
            'description',
            'price',
            'quantity',
            'is_active'
        )
