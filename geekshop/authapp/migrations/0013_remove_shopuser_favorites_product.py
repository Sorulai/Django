# Generated by Django 3.2.8 on 2021-12-13 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_shopuser_favorites_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuser',
            name='favorites_product',
        ),
    ]