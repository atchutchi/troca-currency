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

# Function to retrieve exchange rate from Google Sheets
def get_rate_from_sheet(base_currency, target_currency):
    all_records = WORKSHEET.get_all_records()
    for record in all_records:
        # If a record matches the base and target currency, return the exchange rate
        if record['code'] == base_currency and record['code'] == target_currency:
            return record['exchange_rate']
    return None

# Function to fetch exchange rates using the 'exchangerate.host' API
def get_all_exchange_rates(base_currency):
    url = f'https://api.exchangerate.host/latest?base={base_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

# Function to validate a currency code
def is_valid_currency_code(code):
    return len(code) == 3 and code.isalpha()

# Function to validate the conversion amount
def is_valid_amount(amount):
    try:
        return float(amount) > 0
    except ValueError:
        return False

def save_conversion_to_history(base_currency, target_currency, amount, converted_amount):
    history_record = {
        'base_currency': base_currency,
        'target_currency': target_currency,
        'amount': amount,
        'converted_amount': converted_amount
    }
    HISTORY_WORKSHEET.append_row(list(history_record.values()))

def view_conversion_history():
    # Retrieve all records from the 'history' worksheet
    all_records = HISTORY_WORKSHEET.get_all_records()

    # If no records are present, print a message and return
    if not all_records:
        print("No conversion history found.")
        return

    # Print the conversion history
    print("Conversion History:")
    for record in all_records:
        print(f"From {record['base_currency']} to {record['target_currency']}: {record['original_amount']} -> {record['converted_amount']} at {record['timestamp']}")


def save_conversion_to_history(base_currency, target_currency, amount, converted_amount):
    # Get the current date and time
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

def main():
    print("Welcome to Troca-Currency Converter!")
    while True:
        print("\n1. Convert currency\n2. View conversion history\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            convert_currency()
        elif choice == '2':
            view_conversion_history()
        else:
            print("Invalid choice, please select 1 or 2")

        another_operation = input("\nDo you want to perform another operation? (Y/N): ").upper()
        if another_operation != 'Y':
            break

    # End message after the conversions
    print("Thank you for using Troca-Currency Converter!")

if __name__ == "__main__":
    main()
