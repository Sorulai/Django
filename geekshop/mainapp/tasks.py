import json
from datetime import timedelta

import requests
from geekshop.celery import app


@app.task
def get_currency_beat_celery():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    value = response.json().get('Valute').get('USD').get('Value')
    data = {'valute': []}
    data['valute'].append({
        'USD': value
    })
    with open('./mainapp/json/valute.txt', 'w') as f:
        json.dump(data, f)
