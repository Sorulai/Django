# Generated by Django 3.2.8 on 2021-12-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_favoritesproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_sales',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество покупок'),
        ),
    ]