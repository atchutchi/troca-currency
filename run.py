import requests


def get_all_exchange_rates(base_currency):
    """
    Defines a get exchange rate function, creates a URL to the exchange rate API, 
    and checks if the HTTP response status code is 200 and
    returns a dictionary of currency codes and corresponding rates.
    """
    url = f'https://api.exchangerate.host/latest?base={base_currency}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None