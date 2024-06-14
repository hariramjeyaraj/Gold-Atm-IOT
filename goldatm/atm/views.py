from django.shortcuts import render
import datetime
import requests
import jsons
import base64
import requests
import shortuuid
from django.http import JsonResponse
from django.shortcuts import redirect
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from django.contrib import messages
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
from django.shortcuts import render






def home(request):
    return render(request, 'homepage.html')

def atm(request):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    
    url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    response = requests.get(url)

    # Initialize variables for API data 
    live_price = None
    silver_price = None

    if response.status_code == 200:
        data = response.json()
        live_price = data.get("liveprice")
        silver_price = data.get("silver_price")

    # Render the template with current date, live price, and silver price
    return render(request, 'atmpage.html', {'current_date': current_date, 'live_price': live_price, 'silver_price': silver_price})

def login(request):
    return render(request, 'login.html')



# def otp(request):
#     # phone = phone
#     if request.method == 'POST':
#         otp_entered = request.POST.get('otp')
#         if 'otp' in request.session:
#             otp_generated = request.session['otp']
#             # Make a request to your OTP validation API endpoint
#             validation_api_url = ''

#             payload = {
#                 'otp_entered': otp_entered,
#                 'otp_generated': otp_generated
#             }
#             try:
#                 response = requests.post(validation_api_url, json=payload)
#                 data = response.json()
#                 if data.get('valid', False):
#                     # OTP is valid, redirect to the desired page
#                     del request.session['otp']
#                     messages.success(request, 'OTP verification successful.')
#                     return redirect('categorie')  # Redirect to the desired page
#                 else:
#                     messages.error(request, 'Invalid OTP. Please try again.')
#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f'Failed to validate OTP: {e}')
#         else:
#             messages.error(request, 'OTP expired or not generated. Please try again.')
#     return render(request, 'otp.html')

    # return render(request,'otp.html')
    
def categories(request):
    return render(request, 'categorie.html')

def bullion(request):
    url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    response = requests.get(url)

    # Initialize variables for API data 
    live_price = None

    if response.status_code == 200:
        data = response.json()
        live_price = data.get("liveprice")

    if live_price is not None:
        live_price_half = live_price / 2
        live_price1 = live_price
        live_price2 = live_price * 2
        live_price3 = live_price * 5

        # Format the prices to two decimal places
        live_price_half = f"{live_price_half:.2f}"
        live_price1 = f"{live_price1:.2f}"
        live_price2 = f"{live_price2:.2f}"
        live_price3 = f"{live_price3:.2f}"
    else:
        live_price_half = live_price1 = live_price2 = live_price3 = "N/A"

    return render(request, 'bullion.html', {
        'live_price': live_price_half, 
        'live_price1': live_price1, 
        'live_price2': live_price2, 
        'live_price3': live_price3
    })

# def silver(request):
#     url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
#     response = requests.get(url)

#     # Initialize variables for API data 
#     silver_price = None

#     if response.status_code == 200:
#         data = response.json()
#         silver_price = data.get("silver_price")
        
#     return render(request,'silver.html', {'silver_price': silver_price/100, 'silver_price1': silver_price/100*2, 'silver_price2': silver_price/100*5, 'silver_price3': silver_price/100*10})

def silver(request):
    url = "https://liverates-api.goldcentral.in/api/liveRateFromDbATM"
    response = requests.get(url)
    
    # Initialize variables for API data 
    silver_price = None

    if response.status_code == 200:
        data = response.json()
        silver_price = data.get("silver_price")
        
    if silver_price is not None:
        silver_price = silver_price / 100
        silver_price1 = silver_price * 2
        silver_price2 = silver_price * 5
        silver_price3 = silver_price * 10

        # Format the prices to two decimal places
        silver_price = f"{silver_price:.2f}"
        silver_price1 = f"{silver_price1:.2f}"
        silver_price2 = f"{silver_price2:.2f}"
        silver_price3 = f"{silver_price3:.2f}"
    else:
        silver_price = silver_price1 = silver_price2 = silver_price3 = "N/A"

    return render(request, 'silver.html', {
        'silver_price': silver_price, 
        'silver_price1': silver_price1, 
        'silver_price2': silver_price2, 
        'silver_price3': silver_price3
    })

def product(request):
    weight = request.GET.get('weight')
    price = request.GET.get('price')
    image_url = request.GET.get('image_url')

    # Convert price to float for calculation
    price = float(price)
    
    # Calculate 4% of the price
    percentage_of_price = price * 0.04
    
    # Calculate the total amount
    total_amount = price + percentage_of_price
    print(total_amount)
    
    # Round the values to 2 decimal places for display
    context = {
        'weight': weight,
        'price': price,
        'percentage_of_price': round(percentage_of_price, 2),  # Rounding to 2 decimal places
        'total_amount': round(total_amount, 2),  # Rounding to 2 decimal places
        'image_url': image_url,
    }
    return render(request, 'product.html', context)

def product2(request):
    weight = request.GET.get('weight')
    price = request.GET.get('price')
    image_url = request.GET.get('image_url')

    # Convert price to float for calculation
    price = float(price)
    
    # Calculate 4% of the price
    percentage_of_price = price * 0.04

    total_amount = price + percentage_of_price

    
    context = {
        'weight': weight,
        'price': price,
        'percentage_of_price': round(percentage_of_price, 2),  # Rounding to 2 decimal places
        'total_amount': round(total_amount, 2),  # Rounding to 2 decimal places
        'image_url': image_url,
    }
    return render(request,'product2.html',context)

def calculate_sha256_string(input_string):
   
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()

def base64_encode(input_dict):
   
    json_data = jsons.dumps(input_dict)
    data_bytes = json_data.encode('utf-8')
    return base64.b64encode(data_bytes).decode('utf-8')





client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
def initiate_payment(total_amount, currency='INR'):
    data = {
        'amount': int(total_amount * 100), 
        'currency': currency,
        'payment_capture': '1' 
    }
    response = client.order.create(data=data)
   

def payment_view(request):
    # Get the total amount from the request or any other source

    total_amount = request.GET.get('total_amount')  
    # Convert total_amount to float
    total_amount = float(total_amount)
    
    # Initiating payment with Razorpay
    order_id = initiate_payment(total_amount)
    
    context = {
        'order_id': order_id,
        'total_amount': total_amount
    }
    return render(request, 'payment.html', context)

def payment_success_view(request):
    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('razorpay_payment_id')
    signature = request.POST.get('razorpay_signature')
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        return render(request, 'payment_success.html')
    except razorpay.errors.SignatureVerificationError as e:
        return render(request, 'payment_success.html')













#     MAINPAYLOAD = {
#         "merchantId": "PGTESTPAYUAT73",
#         "merchantTransactionId": shortuuid.uuid(),
#         "merchantUserId": "u123",
#         "amount": 10000,
#         "redirectUrl": "http://127.0.0.1:8000/success/",
#         "redirectMode": "POST",
#         "callbackUrl": "http://127.0.0.1:8000/success/",
#         "mobileNumber": "9999999999",
#         "paymentInstrument": {
#             "type": "PAY_PAGE"
#         }
#     }
   
#     INDEX = "1"
#     ENDPOINT = "/pg/v1/pay"
#     SALTKEY = "c27f072c-3fad-4ccf-95ac-4940f7bfad7d"
    
#     base64String = base64_encode(MAINPAYLOAD)
#     mainString = base64String + ENDPOINT + SALTKEY;
#     sha256Val = calculate_sha256_string(mainString)
#     checkSum = sha256Val + '###' + INDEX;
   
#     headers = {
#         'Content-Type': 'application/json',
#         'X-VERIFY': checkSum,
#         'accept': 'application/json',
#     }
#     json_data = {
#         'request': base64String,
#     }
#     response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
#     responseData = response.json();
#     return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])

# def payment_return(request):
    
#     INDEX = "1"
#     SALTKEY = "c27f072c-3fad-4ccf-95ac-4940f7bfad7d"
   
#     form_data = request.POST
#     form_data_dict = dict(form_data)
#     transaction_id = form_data.get('transactionId', None)

#     if transaction_id:
#         request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT73/' + transaction_id;
#         sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT73/' + transaction_id + SALTKEY;
#         sha256_val = calculate_sha256_string(sha256_Pay_load_String);
#         checksum = sha256_val + '###' + INDEX;
    
#         headers = {
#             'Content-Type': 'application/json',
#             'X-VERIFY': checksum,
#             'X-MERCHANT-ID': transaction_id,
#             'accept': 'application/json',
#         }
#         response = requests.get(request_url, headers=headers)
    


def success(request):
    return render(request,'successfully.html')

def machine(request):
    return render(request,'machine.html')

def thanku(request):
    return render(request,'thanku.html')


   


