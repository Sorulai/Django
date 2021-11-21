from datetime import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    acces_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about', 'photo_200_orig'])
    url_method = 'https://api.vk.com/method/'

    api_url = f'{url_method}users.get?fields={fields}&access_token={acces_token}&v=5.131'

    response = requests.get(api_url)
    if response.status_code != 200:
        return
    print(response.json())
    data_json = response.json()['response'][0]
    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')

        age = datetime.now().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'about' in data_json:
        user.shopuserprofile.about_me = data_json['about']

    if 'photo_200_orig' in data_json:
        img_url = data_json['photo_200_orig']
        # img_name = f'{user.username}.jpg'
        # img = requests.get(img_url).content
        # full_img = f'{settings.MEDIA_ROOT}/users_avatars/{img_name}'
        # with open(full_img, 'wb') as f:
        #     f.write(img)

        # user.avatar = f'users_avatars/{img_name}'
        user.avatar_url = img_url

    user.save()
