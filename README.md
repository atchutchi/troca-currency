# Troca-Currency

## Overview

Troca-Currency is a Python-based application that enables users to convert currencies using real-time exchange rates from the Google Sheets and alternatively 'exchangerate.host' API. Additionally, the application stores the conversion history in a Google Sheets document, providing an easily accessible log of past conversions with Date and Time of the conversion.

[Here is the live version of the project](https://troca-currency-3e6445701967.herokuapp.com/)

![XOX Winners Resposive](./assets/images/site.png)

## Usage
Upon running the script, users will be greeted with a main menu where they can choose to convert currency or view conversion history.

When converting currency, users will be asked to input the base currency, the target currency, and the amount to be converted. If the exchange rate is available, the converted amount will be displayed and stored in the 'history' worksheet in the Google Sheets document.

When viewing conversion history, users will see a list of all past conversions, including the base currency, target currency, original amount, converted amount, and the date and time of conversion.

## Features

## Data Model

## Testing

### Validator Testing
**PEP8CI**
- No error were returned from [pep8ci.herokuapp](https://pep8ci.herokuapp.com/)

## Deployment
This project was deployed using Code Institute's mock terminal for Heroku

- Steps for deployments:
    - Fork on clone this repository
    - Create a new Heroku app
    - Set the buildbacks to Python and NodeJS in order
    - Link the Heroku app to the repository
    - Click on Deploy


## Credits

### Content
- Google Sheets based model taken from [ablebits](https://www.ablebits.com/office-addins-blog/currency-conversion-google-sheets/).

### Media
- Screenshot of the responsive where taken from [ui.dev](https://ui.dev/amiresponsive?url=https://troca-currency-3e6445701967.herokuapp.com/).

### Language Used
- Python

### Codes
- API used for conversion currency [exchangerate.host](https://exchangerate.host/#/)
- [Geeksforgeeks Currency Converter in Python](https://www.geeksforgeeks.org/currency-converter-in-python/)
- [Requests:HTTP](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request)

### Deployment
- Code Institute for the deployment terminar