import requests


def get_all_exchange_rates(base_currency):
    url = f'https://api.exchangerate.host/latest?base={base_currency}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None