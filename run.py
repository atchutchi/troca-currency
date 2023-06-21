import requests


def get_all_exchange_rates(base_currency):
    """
    Fetches the latest exchange rates for the given base currency and
    returns a dictionary of currency codes and corresponding rates.
    """
    url = f'https://api.exchangerate.host/latest?base={base_currency}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None