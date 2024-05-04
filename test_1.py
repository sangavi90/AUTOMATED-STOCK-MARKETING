import http.client
import json
import pyotp

import requests
import json
import pandas
url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
response=requests.get(url,headers=headers)
print(response)


response_text=response.text
print(response_text)
json_object=json.loads(response_text)
# print(type(json_object))
print(json_object.keys())



# class OrderPlacer:
#     def __init__(self, username, pwd, api_key, client_local_ip, client_public_ip, mac_address):
#         self.username = username
#         self.pwd = pwd
#         self.api_key = api_key
#         self.client_local_ip = client_local_ip
#         self.client_public_ip = client_public_ip
#         self.mac_address = mac_address

#     def place_order(self, symbol, quantity, disclosed_quantity, transaction_type, order_type, variety, product_type):
#         try:
#             # Generate TOTP
#             token = "AFH6577WNNSGC4TGXVLJWHVAQI"
#             totp = pyotp.TOTP(token).now()

#             # Generate session
#             jwt_token = self.generate_session(totp)

#             # Prepare payload for placing order
#             payload = {
#                 "exchange": "NSE",
#                 "tradingsymbol": symbol,
#                 "quantity": quantity,
#                 "disclosedquantity": disclosed_quantity,
#                 "transactiontype": transaction_type,
#                 "ordertype": order_type,
#                 "variety": variety,
#                 "producttype": product_type
#             }

#             # Make request to place order
#             response = self.make_order_request(payload, jwt_token)

#             return response
        
#         except Exception as e:
#             error_message = "Error placing order: {}".format(str(e))
#             return error_message

#     def generate_session(self, totp):
#         # Your logic to generate session using username, pwd, and TOTP token
#         # Example: 
#         # session_data = smartApi.generateSession(self.username, self.pwd, totp)
#         # return session_data['data']['jwtToken']
#         pass

#     def make_order_request(self, payload, jwt_token):
#         # Make request to place order
#         headers = {
#             'Authorization': jwt_token,
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'X-UserType': 'USER',
#             'X-SourceID': 'WEB',
#             'X-ClientLocalIP': self.client_local_ip,
#             'X-ClientPublicIP': self.client_public_ip,
#             'X-MACAddress': self.mac_address,
#             'X-PrivateKey': self.api_key
#         }

#         conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
#         conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(payload), headers)
#         res = conn.getresponse()
#         data = res.read().decode("utf-8")

#         # Close connection
#         conn.close()

#         return data

# order_placer = OrderPlacer(username, pwd, api_key, ClientLocalIP, ClientPublicIP, MACAddress)
# response = order_placer.place_order("INFY-EQ", 5, 3, "BUY", "MARKET", "STOPLOSS", "INTRADAY")
# print(response) 





#  if expiry date expired company name,strike_prike and expiry_date also get updated:
# import datetime
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ExpiryDate, CompanyName, Options
# from .utils import fetch_live_data, fetch_expiry_dates

# class OptionsUpdate(APIView):
#     def post(self, request):
#         try:
#             # Fetch live data for expiry dates, company names, and strike prices
#             expiry_dates = fetch_expiry_dates()
#             live_data = fetch_live_data()

#             # Update expiry dates
#             for expiry_date in expiry_dates:
#                 expiry_instance, created = ExpiryDate.objects.get_or_create(expiry_date=expiry_date)
#                 expiry_instance.save()

#             # Update or create records in the database for company names and strike prices
#             for company_name, strike_prices in live_data.items():
#                 company, created = CompanyName.objects.get_or_create(name=company_name)
#                 options, created = Options.objects.get_or_create(company_name=company)
#                 options.strike_prices = strike_prices
#                 options.save()

#             return Response("Options data updated successfully", status=status.HTTP_200_OK)

#         except Exception as e:
#             error_message = "Error updating options data: {}".format(str(e))
#             return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import datetime
from .models import ExpiryDate, CompanyName, Options
from .external_api import fetch_expiry_dates, fetch_live_data

def update_expired_options():
    # Get current date
    current_date = datetime.date.today()

    # Get expired expiry dates
    expired_expiry_dates = ExpiryDate.objects.filter(expiry_date__lt=current_date)

    for expired_expiry_date in expired_expiry_dates:
        # Delete expired expiry date from the database
        expired_expiry_date.delete()

        # Fetch live data for expiry dates, company names, and strike prices
        expiry_dates = fetch_expiry_dates()
        live_data = fetch_live_data()

        # Update expiry dates
        for expiry_date in expiry_dates:
            expiry_instance, created = ExpiryDate.objects.get_or_create(expiry_date=expiry_date)
            expiry_instance.save()

        # Update or create records in the database for company names and strike prices
        for company_name, strike_prices in live_data.items():
            company, created = CompanyName.objects.get_or_create(name=company_name)
            options, created = Options.objects.get_or_create(company_name=company)
            options.strike_prices = strike_prices
            options.save()


# .external_api.py file:
             
import requests
def fetch_expiry_dates():
    # Implement the logic to fetch expiry dates from an external API or source
    # For demonstration purposes, let's assume expiry dates are fetched from a hypothetical API
    expiry_dates_api_url = 'https://example.com/api/expiry-dates'
    
    try:
        response = requests.get(expiry_dates_api_url)
        if response.status_code == 200:
            expiry_dates = response.json().get('expiry_dates', [])
            return expiry_dates
        else:
            print("Failed to fetch expiry dates. Status code:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching expiry dates:", str(e))
        return []

def fetch_live_data():
    # Implement the logic to fetch live data for company names and strike prices
    # For demonstration purposes, let's assume live data is fetched from a hypothetical API
    live_data_api_url = 'https://example.com/api/live-data'
    
    try:
        response = requests.get(live_data_api_url)
        if response.status_code == 200:
            live_data = response.json().get('live_data', {})
            return live_data
        else:
            print("Failed to fetch live data. Status code:", response.status_code)
            return {}
    except Exception as e:
        print("Error fetching live data:", str(e))
        return {}
#  model for expiry date:
from django.db import models

class ExpiryDate(models.Model):
    expiry_date = models.DateField(unique=True)

    def __str__(self):
        return str(self.expiry_date)
    

    #  code for CE and  PE both the expiry date and strike price:
class ExpiryStrikePrice(APIView):
    def get(self, request):
        url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            ce_list = []
            pe_list = []

            if 'records' in data and 'data' in data['records']:
                ce_list = [{'expiry_date': ce['expiryDate'], 'strike_price': ce['strikePrice']} for ce in data['records']['data']['CE']]
                pe_list = [{'expiry_date': pe['expiryDate'], 'strike_price': pe['strikePrice']} for pe in data['records']['data']['PE']]

            return Response({'CE': ce_list, 'PE': pe_list})
        else:
            return Response({'error': 'Failed to fetch data'}, status=response.status_code)
        


        #  this code for expiry date and strike price  update automatically:

import requests
import time
from rest_framework.response import Response
from rest_framework.views import APIView

class ExpiryStrikePrice(APIView):
    ce_list = []
    pe_list = []

    @classmethod
    def update_expiry_strike(cls):
        url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if 'records' in data and 'data' in data['records']:
                cls.ce_list = [{'expiry_date': ce['expiryDate'], 'strike_price': ce['strikePrice']} for ce in data['records']['data']['CE']]
                cls.pe_list = [{'expiry_date': pe['expiryDate'], 'strike_price': pe['strikePrice']} for pe in data['records']['data']['PE']]
            else:
                print("Data format not as expected")
        else:
            print("Failed to fetch data, status code:", response.status_code)

    def get(self, request):
        return Response({'CE': self.ce_list, 'PE': self.pe_list})

    @classmethod
    def continuously_update_data(cls):
        while True:
            cls.update_expiry_strike()
            time.sleep(60)  # Fetch data every minute

# Start continuously updating data in a separate thread
update_thread = threading.Thread(target=ExpiryStrikePrice.continuously_update_data)
update_thread.start()




#  this code for without init and class method ,update expiry,strike :
import requests
import time
from rest_framework.response import Response
from rest_framework.views import APIView

class ExpiryStrikePrice(APIView):
    def get(self, request):
        return Response({'CE': self.ce_list, 'PE': self.pe_list})

def update_expiry_strike():
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        ce_list = []
        pe_list = []

        if 'records' in data and 'data' in data['records']:
            ce_list = [{'expiry_date': ce['expiryDate'], 'strike_price': ce['strikePrice']} for ce in data['records']['data']['CE']]
            pe_list = [{'expiry_date': pe['expiryDate'], 'strike_price': pe['strikePrice']} for pe in data['records']['data']['PE']]

        ExpiryStrikePrice.ce_list = ce_list
        ExpiryStrikePrice.pe_list = pe_list
    else:
        print("Failed to fetch data, status code:", response.status_code)

# Continuously update the data
while True:
    update_expiry_strike()
    time.sleep(60)  # Fetch data every minute


# class ExpiryStrikePrice(APIView):
#     ce_list = []
#     pe_list = []

#     def get(self, request):
#         return Response({'CE': self.ce_list, 'PE': self.pe_list})

# def process_data(json_data):
#     ce_list = []
#     pe_list = []

#     if 'records' in json_data and 'data' in json_data['records']:
#         ce_data = json_data['records']['data'].get('CE', [])
#         pe_data = json_data['records']['data'].get('PE', [])

#         # Ensure ce_data and pe_data are lists
#         ce_data = ce_data if isinstance(ce_data, list) else []
#         pe_data = pe_data if isinstance(pe_data, list) else []


#         # Process CE data
#         for ce in ce_data:
#             expiry_date = ce.get('expiryDate', '')
#             strike_price = ce.get('strikePrice', '')
#             ce_list.append({'expiry_date': expiry_date, 'strike_price': strike_price})

#         # Process PE data
#         for pe in pe_data:
#             expiry_date = pe.get('expiryDate', '')
#             strike_price = pe.get('strikePrice', '')
#             pe_list.append({'expiry_date': expiry_date, 'strike_price': strike_price})


#     return ce_list, pe_list

# def update_expiry_strike():
#     url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()

#         # Process the JSON data
#         ce_data_list, pe_data_list = process_data(data)

#         # Update the class attributes with the fetched data
#         ExpiryStrikePrice.ce_list = ce_data_list
#         ExpiryStrikePrice.pe_list = pe_data_list

#         print("Data updated successfully.")
#     else:
#         print("Failed to fetch data, status code:", response.status_code)

# # Continuously update the data
# while True:
#     update_expiry_strike()
#     time.sleep(60)  # Fetch data every minute



##################################################################################################################3
    

# #  placing the order:
# from SmartApi import SmartConnect
# import pyotp
# from logzero import logger

# def place_order_with_smart_api(api_key, username, pwd, token, correlation_id, symbol, exchange, transaction_type, quantity, price):
#     smartApi = SmartConnect(api_key)
#     try:
#         totp = pyotp.TOTP(token).now()
#     except Exception as e:
#         logger.error("Invalid Token: The provided token is not valid.")
#         raise e

#     data = smartApi.generateSession(username, pwd, totp)

#     if data['status'] == False:
#         logger.error(data)
#     else:
#         authToken = data['data']['jwtToken']
#         refreshToken = data['data']['refreshToken']
#         feedToken = smartApi.getfeedToken()
#         res = smartApi.getProfile(refreshToken)
#         exchanges = res['data']['exchanges']

#         # Check if the exchange is supported
#         if exchange in exchanges:
#             smartApi.generateToken(refreshToken)

#             try:
#                 # Place order
#                 order_params = {
#                     "variety": "NORMAL",
#                     "tradingsymbol": symbol,
#                     "symboltoken": "",  # Fill this if you have the token of the symbol
#                     "transactiontype": transaction_type,
#                     "exchange": exchange,
#                     "ordertype": "LIMIT",
#                     "producttype": "INTRADAY",
#                     "duration": "DAY",
#                     "price": price,
#                     "squareoff": "",
#                     "stoploss": "",
#                     "quantity": quantity,
#                     "triggerprice": "",
#                     "disclosedquantity": "",
#                     "validity": "DAY",
#                     "productCode": ""  # Fill this if you have a product code
#                 }
#                 response = smartApi.placeOrder(order_params)
#                 logger.info(f"Order placed successfully: {response}")

#             except Exception as e:
#                 logger.error(f"Error placing order: {e}")
#         else:
#             logger.error(f"Exchange {exchange} is not supported.")

# # Example usage
# api_key = 'Your Api Key'
# username = 'Your client code'
# pwd = 'Your pin'
# token = "Your QR value"
# correlation_id = "abcde"

# # Example order details
# symbol = 'SBIN'  # Example symbol
# exchange = 'NSE'  # Example exchange
# transaction_type = 'BUY'  # Example transaction type
# quantity = 1  # Example quantity
# price = 350.50  # Example price

# place_order_with_smart_api(api_key, username, pwd, token, correlation_id, symbol, exchange, transaction_type, quantity, price)
    