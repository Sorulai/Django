# Generated by Django 3.2.8 on 2021-11-19 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20211116_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='Возраст'),
        ),
    ]