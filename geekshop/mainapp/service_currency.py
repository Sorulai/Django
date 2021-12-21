import json


def get_currency():
    with open('./mainapp/json/valute.txt') as f:
        data = json.load(f)
        value = data.get('valute')[0].get('USD')
        return round(value, 2)