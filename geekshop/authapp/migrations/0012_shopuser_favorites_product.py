# Generated by Django 3.2.8 on 2021-12-13 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211105_2035'),
        ('authapp', '0011_alter_shopuser_avatar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='favorites_product',
            field=models.ManyToManyField(to='mainapp.Product'),
        ),
    ]
