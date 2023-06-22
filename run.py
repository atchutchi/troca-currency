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


def is_valid_currency_code(code):
    """
    Checks if the input string is a valid 3 letter currency code.
    """
    return len(code) == 3 and code.isalpha()


def main():
    while True:
        # Input Source Currency
        base_currency = input("Enter the base currency (e.g. USD): ").upper()
        if not is_valid_currency_code(base_currency):
            print("Please enter a valid 3-letter currency code.")
            continue


        # Looking for conversion rates for a base currency
        exchange_rates = get_all_exchange_rates(base_currency)
        if not exchange_rates:
            continue


        # Input Target Currency
        target_currency = input("Enter the target currency to convert to (e.g. EUR): ").upper()
        if not is_valid_currency_code(target_currency):
            print("Please enter a valid 3-letter currency code.")
            continue


if __name__ == "__main__":
    # Start
    main()
print("Welcome to Troca-Currency Converter!")
print("Troca-Currency Converter is a straightforward tool for converting currencies.")
print("Enter the base currency, the target currency, and the conversion amount.")
print("Follow the instructions to complete the conversion.\n")