from datetime import timedelta

import requests
from celery import shared_task
from geekshop.celery import app



# @shared_task()
# def get_currency_beat_celery():
#     url = 'https://www.cbr-xml-daily.ru/daily_json.js'
#     response = requests.get(url)
#     value = response.json().get('Valute').get('USD').get('Value')
#     print(value)
#     with open('text.txt', 'w', encoding='utf8') as f:
#         f.write(value)


# def get_currency_celery():
#     # url = 'https://www.cbr-xml-daily.ru/daily_json.js'
#     # response = requests.get(url)
#     # value = response.json().get('Valute').get('USD').get('Value')
#     # print(value)
#     print(5)
#     # with open('text.txt', 'w', encoding='utf8') as f:
#     #     f.write(value)
