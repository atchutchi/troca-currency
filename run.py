# Import the necessary modules
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Define the scope for Google Sheets API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Load credentials from the 'creds.json' file and create a client to interact with Google Sheets
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('exchange_currency')

# Access the 'codes' worksheet from the sheet
WORKSHEET = SHEET.worksheet("codes")

# Access the 'history' worksheet from the sheet
HISTORY_WORKSHEET = SHEET.worksheet("history")


def get_rate_from_sheet(base_currency, target_currency):
    """
    Retrieve exchange rate from Google Sheets.

    The function searches through all records in the Google Sheets document
    to find an exchange rate for the provided base and target currency. 

    Parameters:
    base_currency (str): Code of the base currency.
    target_currency (str): Code of the target currency.

    Returns:
    float: The exchange rate if found. None otherwise.
    """
    all_records = WORKSHEET.get_all_records()
    for record in all_records:
        # If a record matches the base and target currency, return the exchange rate
        if record['code'] == base_currency and record['code'] == target_currency:
            return record['exchange_rate']
    return None


def get_all_exchange_rates(base_currency):
    """
    Fetch exchange rates for the given base currency.

    This function uses the 'exchangerate.host' API to fetch the exchange rates of all 
    currencies relative to the base currency.

    Parameters:
    base_currency (str): The code of the base currency.

    Returns:
    dict: A dictionary of exchange rates if the request is successful. None otherwise.
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
    Validate a currency code.

    Checks if the provided string is a valid currency code. A valid code consists of three alphabetic characters.

    Parameters:
    code (str): The currency code to validate.

    Returns:
    bool: True if the code is valid, False otherwise.
    """
    return len(code) == 3 and code.isalpha()


def is_valid_amount(amount):
    """
    Validate the conversion amount.

    Checks if the provided amount is a valid number and is greater than 0.

    Parameters:
    amount (str): The amount to validate.

    Returns:
    bool: True if the amount is valid, False otherwise.
    """
    try:
        return float(amount) > 0
    except ValueError:
        return False


def save_conversion_to_history(base_currency, target_currency, amount, converted_amount):
    """
    Save a currency conversion to the history worksheet.

    The function creates a new record with the base currency, target currency, conversion amount, and converted amount.
    This record is then appended to the 'history' worksheet in the Google Sheets document.

    Parameters:
    base_currency (str): The code of the base currency.
    target_currency (str): The code of the target currency.
    amount (float): The amount in the base currency that was converted.
    converted_amount (float): The resulting amount in the target currency.
    """
    history_record = {
        'base_currency': base_currency,
        'target_currency': target_currency,
        'amount': amount,
        'converted_amount': converted_amount
    }
    HISTORY_WORKSHEET.append_row(list(history_record.values()))


def view_conversion_history():
    """
    Display the conversion history.

    This function fetches all records from the 'history' worksheet in the Google Sheets document.
    Each record includes the base currency, target currency, original amount, converted amount, and conversion time.
    """
    all_records = HISTORY_WORKSHEET.get_all_records()

    # If no records are present, print a message and return
    if not all_records:
        print("No conversion history found.")

    # Print the conversion history
    print("Conversion History:")
    for record in all_records:
        print(f"From {record['base_currency']} to {record['target_currency']}: {record['original_amount']} -> {record['converted_amount']} at {record['timestamp']}")


def save_conversion_to_history(base_currency, target_currency, amount, converted_amount):
    """
    Save a currency conversion into the history worksheet in Google Sheets.
    Parameters:
    base_currency (str): The base currency code.
    target_currency (str): The target currency code.
    amount (float): The amount to be converted from the base currency.
    converted_amount (float): The converted amount in the target currency.
    """
    now = datetime.now()

    # Format the datetime object to match the format used by Google Sheets
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")

    history_record = {
        'base_currency': base_currency,
        'target_currency': target_currency,
        'amount': amount,
        'converted_amount': converted_amount,
        'timestamp': timestamp
    }
    HISTORY_WORKSHEET.append_row(list(history_record.values()))


def convert_currency():
    """
    Handle the process of currency conversion.

    This function guides the user to input a base currency, target currency, and amount for conversion.
    It validates the input, retrieves the exchange rate, performs the conversion, and displays the result.
    The conversion is then saved to the history.
    """
    while True:
        base_currency = input("Enter the base currency (e.g. USD): ").upper()
        if not is_valid_currency_code(base_currency):
            print("Please enter a valid 3-letter currency code.")
            continue

        target_currency = input("Enter the target currency to convert to (e.g. EUR): ").upper()
        if not is_valid_currency_code(target_currency):
            print("Please enter a valid 3-letter currency code.")
            continue

        amount = input("Enter the amount to be converted: ")
        if not is_valid_amount(amount):
            print("Please enter a valid positive number.")
            continue

        amount = float(amount)

        # Try to get the rate from the Google Sheet first
        rate = get_rate_from_sheet(base_currency, target_currency)

        if rate is None:
            # If the rate is not in the sheet, use the API
            exchange_rates = get_all_exchange_rates(base_currency)
            if exchange_rates:
                rate = exchange_rates.get(target_currency)

        if rate:
            # If the rate is obtained, perform the conversion
            converted_amount = rate * amount
            print(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}.")

            # Save the conversion to the history
            save_conversion_to_history(base_currency, target_currency, amount, converted_amount)
        else:
            print(f"Exchange rate for {target_currency} not available.")

        break


def get_and_print_currency_list():
    """
    Fetch and display list of available currencies from the 'codes' worksheet.

    This function retrieves all records from the 'codes' worksheet in the Google Sheets document
    and prints the country name and corresponding currency code for each record.
    """
    all_records = WORKSHEET.get_all_records()
    # Print the list of available currencies
    print("Available Currencies:")
    for record in all_records:
        print(f"{record['country_name']}: {record['code']}")


def main():
    """
    The main function that runs the currency conversion program.

    This function handles the user interface, prompting the user to make choices and providing feedback.
    It loops until the user decides to stop the program.
    """
    print("Welcome to Troca-Currency Converter!")
    while True:
        while True:
            print("\n1. Convert currency\n2. View conversion history\n3. View list of available currencies\n")
            choice = input("Enter your choice: ")

            if choice == '1':
                convert_currency()
                break
            elif choice == '2':
                view_conversion_history()
                break
            elif choice == '3':
                get_and_print_currency_list()
                break
            else:
                print("Invalid choice!\nPlease select 1, 2 or 3:")

        while True:
            another_operation = input("\nDo you want to perform another operation? (Y/N): ").upper()
            if another_operation == 'Y':
                break
            elif another_operation == 'N':
                print("Thank you for using Troca-Currency Converter!")
                return
            else:
                print("Invalid input!\nPlease enter Y or N")

    # End message after the conversions
    print("Thank you for using Troca-Currency Converter!")


if __name__ == "__main__":
    main()
