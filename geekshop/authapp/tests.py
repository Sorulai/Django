from django.conf import settings
from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from authapp.models import ShopUser


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekshop'

    def setUp(self) -> None:
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
        )
        self.user = ShopUser.objects.create_user(username='tarantino',
                                                 email='tarantino@geekshop.local',
                                                 password='geekbrains')

        self.user_with__first_name = ShopUser.objects.create_user(username='umaturman',
                                                                  email='umaturman@geekshop.local',
                                                                  password='geekbrains',
                                                                  first_name='Ума')

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь', status_code=self.status_ok)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=self.status_ok)

    def test_logout(self):
        self.client.login(username='tarantino', password='geekbrains')

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

        new_user = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'
        }
        response = self.client.post('/auth/register/', data=new_user)
        self.assertEqual(response.status_code, self.status_redirect)

        new_user1 = ShopUser.objects.get(username=new_user['username'])

        activation_url = f"http://localhost:8088/auth/verify/{new_user['email']}/{new_user1.activate_key}/"
        self.client.get(activation_url)
        self.client.login(username=new_user['username'],
                         password=new_user['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

