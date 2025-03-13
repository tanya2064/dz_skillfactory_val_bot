import json
import requests
from config import API_KEY, keys

class APIException(Exception):
    pass

class ValuteConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str) -> str:
        try:
            if quote == base:
                raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

            if quote not in keys or base not in keys:
                raise APIException('Укажите корректные валюты.')

            try:
                amount = float(amount)
            except ValueError:
                raise APIException('Количество валюты должно быть числом.')

            url = f"https://api.apilayer.com/currency_data/convert?to={keys[base]}&from={keys[quote]}&amount={amount}"
            headers = {"apikey": API_KEY}
            r = requests.get(url, headers=headers)
            data = json.loads(r.content)

            if "result" not in data:
                raise APIException('Ошибка при получении данных от API.')

            total_base = data["result"]
            return f'Цена {amount} {quote} в {base}: {total_base:.2f}'

        except APIException as e:
            return f'Ошибка пользователя:\n{e}'
        except Exception as e:
            return f'Неизвестная ошибка: {e}'