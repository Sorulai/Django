# Generated by Django 3.2.8 on 2021-11-19 17:54

from django.db import migrations


def forwards_func(apps, schema_editor):
    users = apps.get_model('authapp', 'ShopUser')
    userProfile = apps.get_model('authapp', 'ShopUserProfile')
    users = users.objects.all()
    for user in users:
        userProfile.objects.create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0004_shopuserprofile'),
    ]

    operations = [
        migrations.RunPython(code=forwards_func)
    ]
