import requests
import json
from Config import keys


class ConvertionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: float):

        if quote == base:
            raise ConvertionExeption(
                f'Вы ввели одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]

        except KeyError:
            raise ConvertionExeption(f'Ошибка конвертации {quote}.')

        try:
            base_ticker = keys[base]

        except KeyError:
            raise ConvertionExeption(f'Ошибка конвертации {base}.')

        try:
            amount = float(amount)

        except ValueError:
            raise ConvertionExeption(
                f'Неверно указано количество {amount}. ')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
