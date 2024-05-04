from django.http import JsonResponse
from rest_framework.views import APIView
from .imports import *
import http.client
from django.http import JsonResponse
from rest_framework.views import APIView
import pyotp
from .models import Leg
import time




##############

# tasks.py


from .models import Leg
import http.client
import json
import pyotp
from .imports import smartApi, username, pwd


class Order_on_ltp(APIView):
        def post(self,request):
            print("clery executing")
            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                logger.error("Invalid Token: The provided token is not valid.")
                raise e

            # Generate session and obtain JWT token
            data = smartApi.generateSession(username, pwd, totp)
            # netpos = smartApi.position()

            # print("netpos= ",netpos)
            jwt_token = data['data']['jwtToken']

            headers = {
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-UserType': 'USER',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': '192.168.0.116',
                    'X-ClientPublicIP': '49.205.145.221',
                    'X-MACAddress': '80-38-FB-B9-EE-20',
                    'X-PrivateKey': '4dPdQcGs'
                }

            # Make API requests for each Leg object

            i=0
            for leg in Leg.objects.filter(ltp_status="matching.."):
                conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
                payload = {
                    "exchange": 'NSE',
                    "symboltoken": leg.nse_symboltoken
                }

                print(payload)
                
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payload), headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                print(data_dict)

                # Compare LTP with stored price
                ltp = data_dict['data']['ltp']

                print("ltp is =",ltp)
                print(leg)

                while float(leg.price)== ltp:
 ######             # Update order status to 'placed'##########################
                    # payloads = {
                    # "exchange": leg.exchange,
                    # "symboltoken": leg.symboltoken
                    #  }
                    # conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers) #To get ltp data of contract based NFO
                    # res = conn.getresponse()
                    # data = res.read().decode("utf-8")
                    # data_dict = json.loads(data)

                    # print(data_dict)

                    # # Compare LTP with stored price
                    # orderltp = data_dict['data']['ltp']

                    # print("ltp of order price is  =",orderltp)
    
       
                    
                    conn = http.client.HTTPSConnection(
                        "apiconnect.angelbroking.com"
                        )


                    ######################################

                    payload = {
                            "variety": leg.variety,
                            "tradingsymbol": leg.tradingsymbol,
                            "symboltoken": leg.symboltoken,
                            "transactiontype": leg.transactiontype.upper(),
                            "exchange":leg.exchange,
                            "ordertype":leg.ordertype,
                            "producttype": leg.producttype,
                            "duration": leg.duration,
                            #"price": str(orderltp),
                            "squareoff": '0',
                            #"stoploss": "9.5",
                            "quantity": str(leg.quantity),
                            #"triggerprice": "11.5",
                            "expirydate": leg.expirydate,
                            "strikeprice": leg.strikeprice,
                            "instrumenttype":"OPTSTK", #newl added fields
                            "optiontype":leg.optiontype,  
                            # "targetprice":"" o
                        }
        
                    
        

                    
                    # Convert payload to JSON string
                    payload_str = json.dumps(payload)

                    print(payload_str)

                    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
                    res = conn.getresponse()
                    print("hi",res,type(res))
                    data = res.read().decode("utf-8")
                    
                    print(json.loads(data))
                    i+=1
        
                    
                    leg.orderid=json.loads(data)['data']['orderid']
                    leg.uniqueorderid=json.loads(data)['data']["uniqueorderid"]
                    leg.ltp_status = 'placed'
                    
                    leg.save()

            return Response("LTP checking and updating completed successfully{i}")



class trigger_on_ltp(APIView):
        def post(self,request):
            print("trigger executing")
            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                logger.error("Invalid Token: The provided token is not valid.")
                raise e

            # Generate session and obtain JWT token
            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            headers = {
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-UserType': 'USER',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': '192.168.0.116',
                    'X-ClientPublicIP': '49.205.145.221',
                    'X-MACAddress': '80-38-FB-B9-EE-20',
                    'X-PrivateKey': '4dPdQcGs'
                }

            # Make API requests for each Leg object
            for leg in Leg.objects.filter(triggerstatus="matching.."):
                conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
                payload = {
                    "exchange": 'NSE',
                    "symboltoken": leg.nse_symboltoken
                }
               
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payload), headers) #to get ltp data of NSE
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                print(data_dict)

                # Compare LTP with stored price
                ltp = data_dict['data']['ltp']

                print("ltp is =",ltp)
            

                if float(leg.triggerprice)>= ltp:
                    # Update order status to 'placed'
                    payloads = {
                    "exchange": leg.exchange,
                    "symboltoken": leg.symboltoken
                     }
                    conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers) #To get ltp data of contract based NFO
                    res = conn.getresponse()
                    data = res.read().decode("utf-8")
                    data_dict = json.loads(data)

                    print(data_dict)

                    # Compare LTP with stored price
                    triggerltp = data_dict['data']['ltp']

                    print("ltp of triggered price is  =",triggerltp)
    
       
        

                    
                    # Convert payload to JSON string
                    # payload_str = json.dumps(payload)

                    # print(payload_str)

                    
                    
                    conn = http.client.HTTPSConnection(
                        "apiconnect.angelbroking.com"
                        )
                    payloadt = {  
                       "variety":leg.variety,
                        "orderid": leg.orderid,
                        "ordertype":leg.ordertype,
                        "producttype":leg.producttype,
                        "duration":leg.duration,
                        "price":leg.placed_price,
                        "triggerprice":triggerltp,
                        "exchange":leg.exchange,
                        "symboltoken":leg.symboltoken,
                        "tradingsymbol":leg.tradingsymbol,
                        "quantity":leg.quantity,
                        

                        
                    }
                    
                    print(payloadt)
                    conn.request("POST","/rest/secure/angelbroking/order/v1/modifyOrder",
                    json.dumps(payloadt), 
                    headers)  # HERE modifying the order and assigning the NFO ltp price
                    
                    
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))
                    
                    
                    leg.triggerstatus = 'triggered'
                    leg.save()

            return Response("LTP checking and triggered completed successfully")

class squareofff(APIView):
     def get(self,request):
          
            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                logger.error("Invalid Token: The provided token is not valid.")
                raise e

            # Generate session and obtain JWT token
            data = smartApi.generateSession(username, pwd, totp)
            netpos = smartApi.position()

            #print("netpos= ",netpos)


            if netpos['data'] != None : 
                for o in netpos['data'] :
                    print(o['netqty'])
                    if int(o['netqty']) != 0 : 
                        transactiontype = "SELL" if int(o['netqty']) > 0 else "BUY"
                        trying=self.place_order(o["tradingsymbol"],o['symboltoken'], transactiontype,o['exchange'],o['producttype'], abs(int(o['netqty'])))
                        time.sleep(0.2)
                        print("kddndn=",trying)
                
                return Response(netpos)

            else:
                return Response("kkm")
     
     def place_order(self,tradingsymbol, symboltoken, transactiontype, exc, producttype, quantity): 
            
            print("fndljnfljdnfld")

            
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
                orderId=smartApi.placeOrder(orderparams)

                print(orderId)
                return True
                
            except Exception as e :
                
                print(e)
          


# obj=SmartConnect(api_key=api_key)
# data = obj.generateSession(username,pwd)

# def place_order( tradingsymbol, symboltoken, transactiontype, exc, producttype, quantity): 
#     try: 
#         orderparams = {
#             "variety": "NORMAL",
#             "tradingsymbol": tradingsymbol,
#             "symboltoken": symboltoken,
#             "transactiontype": transactiontype,
#             "exchange": exc,
#             "ordertype": "MARKET",
#             "producttype": producttype,
#             "duration": "DAY",
#             "price": "0",
#             "squareoff": "0",
#             "stoploss": "0",
#             "quantity": quantity
#             }
#         orderId=obj.placeOrder(orderparams)
        
#     except Exception as e :
        # print(e)

# netpos = obj.position()

# if netpos['data'] != None : 
#     for o in netpos['data'] :
#         if int(o['netqty']) != 0 : 
#             transactiontype = "SELL" if int(o['netqty']) > 0 else "BUY"
#             place_order(o["tradingsymbol"],o['symboltoken'], transactiontype,o['exchange'],o['producttype'], abs(int(o['netqty'])))
#             time.sleep(0.2)