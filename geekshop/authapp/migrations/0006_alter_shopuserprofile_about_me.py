# Generated by Django 3.2.8 on 2021-11-19 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_auto_20211119_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuserprofile',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='Обо мне'),
        ),
    ]
