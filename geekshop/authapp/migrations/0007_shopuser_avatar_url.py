# Generated by Django 3.2.8 on 2021-11-21 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_shopuserprofile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='avatar_url',
            field=models.TextField(blank=True, verbose_name='Ссылка на картинку'),
        ),
    ]
