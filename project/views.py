from django.shortcuts import render
from django.http import HttpResponse
from django.middleware.csrf import get_token
import urllib.request
import xml.etree.ElementTree as ET

def get_exchange_rates():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    with urllib.request.urlopen(url) as response:
        data = response.read()

    root = ET.fromstring(data)
    currency_data = root.findall('.//{*}Cube[@currency][@rate]')
    rates = {item.attrib['currency']: float(item.attrib['rate']) for item in currency_data}
    # EUR nu e prezent in XML
    rates['EUR'] = 1.0 

    # Filtrare valute
    allowed_currencies = ['RON', 'EUR', 'USD', 'GBP', 'CHF', 'BGN', 'HUF']
    rates = {currency: rate for currency, rate in rates.items() if currency in allowed_currencies}

    return rates

def home(request):
    rates = get_exchange_rates()
    csrf_token = get_token(request)

    if request.method == 'POST':
        amount = float(request.POST['amount'])
        from_currency = request.POST['from_currency']
        converted_amounts = {
            currency: round(amount / rates[from_currency] * rate, 4) 
            for currency, rate in rates.items()
        }
        converted_amounts_html = ''.join(
            f'<p style="padding-left: 20px;">{currency}: {amount}</p>' 
            for currency, amount in converted_amounts.items()
        )
    else:
        converted_amounts_html = ''

    response_content = (
        f'<form method="post" style="padding: 20px;">'
        f'<h1>Conversie valutara</h1>'
        f'<input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">'
        f'<input type="number" name="amount" step="0.01" required style="height: 30px;" placeholder="Suma de schimbat">'
        f'<select name="from_currency" style="height: 30px;">'
        f'{"".join(f"<option value={currency}>{currency}</option>" for currency in rates.keys())}'
        f'</select><br><br>'
        f'<input type="submit" value="Schimba">'
        f'</form>'
        f'{converted_amounts_html}'
    )

    return HttpResponse(response_content)