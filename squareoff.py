# from .models import Leg
import http.client
import json
import pyotp
from SmartApi import SmartConnect
# from .imports import  username, pwd
from django.http import JsonResponse
from rest_framework.views import APIView
from .imports import *
import http.client
from django.http import JsonResponse
from rest_framework.views import APIView
import pyotp
from .models import Leg
import time
api_key = '4dPdQcGs'
username = 'S2098754'
pwd = '2024'
smartApi = SmartConnect(api_key)
token = "AFH6577WNNSGC4TGXVLJWHVAQI"
import pyotp





obj=SmartConnect(api_key=api_key)
data = obj.generateSession(username,pwd)

def place_order( tradingsymbol, symboltoken, transactiontype, exc, producttype, quantity): 
    try: 
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": transactiontype,
            "exchange": exc,
            "ordertype": "MARKET",
            "producttype": producttype,
            "duration": "DAY",
            "price": "0",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": quantity
            }
        #orderId=obj.placeOrder(orderparams)  we need thid thing for cancelling the order
        
    except Exception as e :
        print(e)

netpos = obj.position()

print(netpos)

if netpos['data'] != None : 
    for o in netpos['data'] :
        if int(o['netqty']) != 0 : 
            transactiontype = "SELL" if int(o['netqty']) > 0 else "BUY"
            place_order(o["tradingsymbol"],o['symboltoken'], transactiontype,o['exchange'],o['producttype'], abs(int(o['netqty'])))
            time.sleep(0.2)