# Generated by Django 3.2.8 on 2021-11-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_shopuser_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='avatar_url',
            field=models.URLField(blank=True, verbose_name='Ссылка на аватар'),
        ),
    ]