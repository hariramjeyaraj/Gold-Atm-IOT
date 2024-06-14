from django.shortcuts import render
import datetime
import requests
import jsons
import base64
import shortuuid
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from .aws_mqtt import connect, publish_message, disconnect



def home(request):
    return render(request, 'homepage.html')

def atm(request):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    response = requests.get(url)

    live_price = None
    silver_price = None

    if response.status_code == 200:
        data = response.json()
        live_price = data.get("liveprice")
        silver_price = data.get("silver_price")

    return render(request, 'atmpage.html', {'current_date': current_date, 'live_price': live_price, 'silver_price': silver_price})

def login(request):
    return render(request, 'login.html')

def categories(request):
    return render(request, 'categorie.html')

def bullion(request):
    # URLs for fetching live prices and stock information
    live_price_url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    stock_url_template = "http://stg-api.goldatm.gold:3001/api/singleatmstock/atmid"

    # Replace with your actual ATM ID
    atm_id = "GS000002-2024-XYUG-V1-91"
    stock_url = stock_url_template.replace("atmid", atm_id)

    # Fetch live price
    live_price_response = requests.get(live_price_url)
    live_price = None

    if live_price_response.status_code == 200:
        data = live_price_response.json()
        live_price = data.get("liveprice")

    # Fetch stock information
    stock_response = requests.get(stock_url)
    stock_data = []

    if stock_response.status_code == 200:
        stock_data = stock_response.json()
        # print(stock_data,'stock data')


    # Extract stock availability
    stock_availability = {item['grams']: True for item in stock_data if item['status'] == 1 and item['type'] == 'Gold'}

    # Calculate prices for different weights
    if live_price is not None:
        live_price_half = f"{(live_price / 2):.2f}"
        live_price1 = f"{live_price:.2f}"
        live_price2 = f"{(live_price * 2):.2f}"
        live_price5 = f"{(live_price * 5):.2f}"
    else:
        live_price_half = live_price1 = live_price2 = live_price5 = "N/A"

    # Prepare product data with stock availability
    product_data = [
        (0.5, live_price_half, 'G1.png', 'G1-disable.png', stock_availability.get(0.5, False)),
        (1, live_price1, 'G2.png', 'G2-disable.png', stock_availability.get(1, False)),
        (2, live_price2, 'G3.png', 'G3-disable.png', stock_availability.get(2, False)),
        (5, live_price5, 'G4.png', 'G4-disable.png', stock_availability.get(5, False)),
        # (10, live_price5, 'G4.png', 'G4-disable.png', stock_availability.get(10, False)),
    ]

    return render(request, 'bullion.html', {'product_data': product_data})

def silver(request):
    # URLs for fetching live prices and stock information
    live_price_url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    stock_url_template = "http://stg-api.goldatm.gold:3001/api/singleatmstock/atmid"

    # Replace with your actual ATM ID
    atm_id = "GS000002-2024-XYUG-V1-91"
    stock_url = stock_url_template.replace("atmid", atm_id)

    # Fetch live price
    live_price_response = requests.get(live_price_url)
    silver_price = None

    if live_price_response.status_code == 200:
        data = live_price_response.json()
        silver_price = data.get("silver_price")

    # Fetch stock information
    stock_response = requests.get(stock_url)
    stock_data = []

    if stock_response.status_code == 200:
        stock_data = stock_response.json()
        # print(stock_data,'stock data')


    # Extract stock availability
    stock_availability = {item['grams']: True for item in stock_data if item['status'] == 1 and item['type'] == 'Silver'}

    # Calculate prices for different weights
    if silver_price is not None:
        silver_price = silver_price / 100
        silver_price1 = silver_price * 2
        silver_price2 = silver_price * 5
        silver_price3 = silver_price * 10

        silver_price = f"{silver_price:.2f}"
        silver_price1 = f"{silver_price1:.2f}"
        silver_price2 = f"{silver_price2:.2f}"
        silver_price3 = f"{silver_price3:.2f}"
    else:
        silver_price = silver_price1 = silver_price2 = silver_price3 = "N/A"

    # Prepare product data with stock availability
    product_data = [
        (10, silver_price, 'S10.png', 'S10-disable.png', stock_availability.get(10, False)),
        (20, silver_price1, 'S20.png', 'S20-disable.png', stock_availability.get(20, False)),
        (50, silver_price2, 'S50.png', 'S50-disable.png', stock_availability.get(50, False)),
        (100, silver_price3, 'S100.png', 'S100-disable.png', stock_availability.get(100, False)),
    ]

    return render(request, 'silver.html', {'product_data': product_data})
def product(request):
    weight = request.GET.get('weight')
    price = request.GET.get('price')
    image_url = request.GET.get('image_url')

    price = float(price)
    percentage_of_price = price * 0.04
    total_amount = price + percentage_of_price

    context = {
        'weight': weight,
        'price': price,
        'percentage_of_price': round(percentage_of_price, 2),
        'total_amount': round(total_amount, 2),
        'image_url': image_url,
    }
    return render(request, 'product.html', context)

def product2(request):
    weight = request.GET.get('weight')
    price = request.GET.get('price')
    image_url = request.GET.get('image_url')

    price = float(price)
    percentage_of_price = price * 0.04
    total_amount = price + percentage_of_price

    context = {
        'weight': weight,
        'price': price,
        'percentage_of_price': round(percentage_of_price, 2),
        'total_amount': round(total_amount, 2),
        'image_url': image_url,
    }
    return render(request, 'product2.html', context)

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
def initiate_payment(total_amount, currency='INR'):
    data = {
        'amount': total_amount,  # Amount in paise (already converted to integer)
        'currency': currency,
        'payment_capture': '1'
    }
    response = client.order.create(data=data)
    return response['id']

def payment_view(request):       # payment integration final 
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        grams = request.POST.get('grams')
        item_type = request.POST.get('type')
        print(f"Total amount received: {total_amount}, Item type: {item_type}")

        if not total_amount:
            return HttpResponseBadRequest('Total amount is not provided')
        
        try:
            total_amount = float(total_amount)
        except ValueError:
            return HttpResponseBadRequest('Invalid total amount')
        
        final_amount = int(total_amount * 100)  # Convert to paise
        print(f"Final amount in paise: {final_amount}")

        order_id = initiate_payment(final_amount)  # Pass the final_amount in paise
        
        context = {
            'order_id': order_id,
            'total_amount': final_amount,  # Pass amount in paise to the template
            'grams': grams,
            'type': item_type  # Include the type in the context
        }
        print(f"Context passed to template: {context}")
        return render(request, 'payment.html', context)

@csrf_exempt
def payment_success_view(request):
    # Retrieve dynamic values from the request or other sources
    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('razorpay_payment_id')
    signature = request.POST.get('razorpay_signature')
    total_amount = request.POST.get('total_amount')
    grams = request.POST.get('grams')
    item_type = request.POST.get('type')
    mode = request.POST.get('mode', 'UPI')  # Default to 'UPI' if not provided
    pincode = request.POST.get('pincode', 533229)  # Default to 533229 if not provided
    transaction_id = shortuuid.uuid()
    note = request.POST.get('note', 'Default Note')  # Default to 'Default Note' if not provided
    tax_amount = request.POST.get('tax_amount', 233)  # Default to 233 if not provided
    coin_rate = request.POST.get('coin_rate', 23232)  # Default to 23232 if not provided
    card_charges = request.POST.get('card_charges', 0)  # Default to 0 if not provided
    atm_id = request.POST.get('atmid', 'GS000002-2024-XYUG-V1-91')  # Default to a specific ATM ID if not provided

    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        transaction_details = {
            'amount': total_amount,
            'mode': mode,
            'atmid': atm_id,
            'pincode': pincode,
            'transactionid': transaction_id,
            'note': note,
            'type': item_type,
            'grams': grams,
            'taxAmount': tax_amount,
            'coinRate': coin_rate,
            'cardCharges': card_charges
        }
        print(transaction_details, 'transaction details')

        transaction_response = requests.post('http://stg-api.goldatm.gold:3001/api/transaction', json=transaction_details)
        print(transaction_response, 'response coming')

        if transaction_response.status_code == 200:
            transaction_data = transaction_response.json()
            print(transaction_data, 'transaction data')

            stock_update_details = {
                'atmid': atm_id,
                'type': item_type,
                'grams': grams  # Update to use dynamic grams value
            }
            print(stock_update_details, 'stock update details')

            stock_update_response = requests.post('http://stg-api.goldatm.gold:3001/api/updatestocks', json=stock_update_details)
            stockupdate_data = stock_update_response.json()
            print(stockupdate_data, 'stock update data')

            if stock_update_response.status_code == 200:
                coil_id = stockupdate_data.get('coil_id')
                if coil_id:
                    connect()
                    publish_message(coil_id)
                    disconnect()
            else:
                print('Stock update failed')

        else:
            print('Transaction failed')

    except razorpay.errors.SignatureVerificationError as e:
        print(f'Signature verification error: {e}')

    disconnect()
    return render(request, 'payment_success.html')


def success(request):
    return render(request, 'successfully.html')

def machine(request):
    return render(request, 'machine.html')

def thanku(request):
    return render(request, 'thanku.html')
