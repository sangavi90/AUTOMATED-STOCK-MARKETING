from app.imports import *
# from django.conf import settings
# from angelproject.settings import api_key
from angelproject import settings



# #### manually we post the order:
class PlaceOrderAPIView(APIView):
    def post(self, request):
        print("data is ",request.data)
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
            # print(totp)
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        # correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)

        print(data)
        jwt_token = data['data']['jwtToken']
        # print(jwt_token)
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        #payload = "{\n \"exchange\": \"NSE\",\n    \"tradingsymbol\": \"INFY-EQ\",\n    \"quantity\": 5,\n    \"disclosedquantity\": 3,\n    \"transactiontype\": \"BUY\",\n    \"ordertype\": \"MARKET\", \n    \"variety\": \"STOPLOSS\",  \n    \"producttype\": \"INTRADAY\"  \n}"
        payload={
                    "variety":"NORMAL",
                    "tradingsymbol":"SBICARD25APR24590CE",
                    "symboltoken":"130623",
                    "transactiontype":"BUY",
                    "exchange":"NFO",

                    "ordertype":"MARKET",
                    "producttype":"CARRYFORWARD",
                    "duration":"DAY",
                    #"price":"", #ENTRY PRICE same as trigger price(notification price)
                    "squareoff":"0",
                    "stoploss":"0",
                    "quantity":"800",
                    "instrumenttype":"OPTSTK", #newl added fields
                    "optiontype":"CE",     #newly added  fields

                    #"triggerprice":"740",
                    "expirydate":"25APR2024",
                    "strikeprice":"590.000000"
                    }  
        
        # payload={"variety": "NORMAL",
        #           "tradingsymbol": "TATACHEM25APR24990CE",
        #             "symboltoken": "137639", 
        #             "transactiontype": "buy",
        #               "exchange": "NFO",
        #                 "ordertype": "LIMIT",
        #                   "producttype": "INTRADAY",
        #                     "duration": "IOC", 
        #                     "price": "234", 
        #                     "squareoff": "0",
        #                       "stoploss": "230",
        #                         "quantity": "6600",
        #                           "triggerprice": "0",
        #                             "expirydate": "30MAY2024",
        #                               "strikeprice": "990.000000"}
        

        headers = {
            'Authorization':jwt_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP':'192.168.0.108',
            'X-ClientPublicIP':'49.205.145.221',
            'X-MACAddress':'80-38-FB-B9-EE-20',
            'X-PrivateKey':'4dPdQcGs'
        }

        # Convert payload to JSON string
        payload_str = json.dumps(payload)

        print(payload_str)

        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
        res = conn.getresponse()
        print("hi",res,type(res))
        data = res.read().decode("utf-8")
        print("hgyeullovvyv",data)
        print(json.loads(data))
        
        
        return Response(json.loads(data))
    

    

###############################################################################################











# # #  /######## multiple leg order placede:
# class multiple_legs(APIView):
#     def post(self, request):
#         try:
#             token = "AFH6577WNNSGC4TGXVLJWHVAQI"
#             totp = pyotp.TOTP(token).now()
#         except Exception as e:
#             logger.error("Invalid Token: The provided token is not valid.")
#             raise e

#         data = smartApi.generateSession(username, pwd, totp)
#         jwt_token = data['data']['jwtToken']
#         conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

#         # Get orders from the request data
#         orders = request.data.get("orders", [])

#         response_data = []
#         for order in orders:
#             try:
#                 # Extracting required fields from the order
#                 variety = order.get("variety")
#                 tradingsymbol = order.get("tradingsymbol")
#                 symboltoken = order.get("symboltoken")
#                 transactiontype = order.get("transactiontype")
#                 exchange = order.get("exchange")
#                 ordertype = order.get("ordertype")
#                 producttype = order.get("producttype")
#                 duration = order.get("duration")
#                 price = order.get("price")
#                 squareoff = order.get("squareoff")
#                 stoploss = order.get("stoploss")
#                 quantity = order.get("quantity")
#                 triggerprice = order.get("triggerprice")
#                 expirydate = order.get("expirydate")
#                 strikeprice = order.get("strikeprice")

#                 payload = {
#                     "variety": variety,
#                     "tradingsymbol": tradingsymbol,
#                     "symboltoken": symboltoken,
#                     "transactiontype": transactiontype,
#                     "exchange": exchange,
#                     "ordertype": ordertype,
#                     "producttype": producttype,
#                     "duration": duration,
#                     "price": price,
#                     "squareoff": squareoff,
#                     "stoploss": stoploss,
#                     "quantity": quantity,
#                     "triggerprice": triggerprice,
#                     "expirydate": expirydate,
#                     "strikeprice": strikeprice
#                 }

#                 payload_str = json.dumps(payload)
#                 headers = {
#                     'Authorization': jwt_token,
#                     'Content-Type': 'application/json',
#                     'Accept': 'application/json',
#                     'X-UserType': 'USER',
#                     'X-SourceID': 'WEB',
#                     'X-ClientLocalIP': '192.168.0.101',
#                     'X-ClientPublicIP': '49.205.145.221',
#                     'X-MACAddress': '80-38-FB-B9-EE-20',
#                     'X-PrivateKey': '4dPdQcGs'
#                 }

#                 conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
#                 res = conn.getresponse()
#                 data = res.read().decode("utf-8")
#                 response_data.append(json.loads(data))
#             except Exception as e:
#                 # Handle exceptions for individual orders if needed
#                 response_data.append({"error": str(e)})
        
#         return Response(response_data)
    

  
# # class multiple_legs(APIView):
# #     def post(self, request):
# #         try:
# #             token = "AFH6577WNNSGC4TGXVLJWHVAQI"
# #             totp = pyotp.TOTP(token).now()
# #         except Exception as e:
# #             logger.error("Invalid Token: The provided token is not valid.")
# #             raise e

# #         data = smartApi.generateSession(username, pwd, totp)
# #         jwt_token = data['data']['jwtToken']
# #         conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

# #         # Get orders from the request data
# #         orders = request.data.get("orders", [])

# #         response_data = []
# #         for order in orders:
# #             try:
# #                 payload = {
# #                     "variety": order.get("variety"),
# #                     "tradingsymbol": order.get("tradingsymbol"),
# #                     "symboltoken": order.get("symboltoken"),
# #                     "transactiontype": order.get("transactiontype"),
# #                     "exchange": order.get("exchange"),
# #                     "ordertype": order.get("ordertype"),
# #                     "producttype": order.get("producttype"),
# #                     "duration": order.get("duration"),
# #                     "price": order.get("price"),
# #                     "squareoff": order.get("squareoff"),
# #                     "stoploss": order.get("stoploss"),
# #                     "quantity": order.get("quantity"),
# #                     "triggerprice": order.get("triggerprice"),
# #                     "expirydate": order.get("expirydate"),
# #                     "strikeprice": order.get("strikeprice")
# #                 }

# #                 payload_str = json.dumps(payload)
# #                 headers = {
# #                     'Authorization': jwt_token,
# #                     'Content-Type': 'application/json',
# #                     'Accept': 'application/json',
# #                     'X-UserType': 'USER',
# #                     'X-SourceID': 'WEB',
# #                     'X-ClientLocalIP': '192.168.0.101',
# #                     'X-ClientPublicIP': '49.205.145.221',
# #                     'X-MACAddress': '80-38-FB-B9-EE-20',
# #                     'X-PrivateKey': '4dPdQcGs'
# #                 }

# #                 conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
# #                 res = conn.getresponse()
# #                 data = res.read().decode("utf-8")
# #                 response_data.append(json.loads(data))
# #             except Exception as e:
# #                 # Handle exceptions for individual orders if needed
# #                 response_data.append({"error": str(e)})
        
# #         return Response(response_data)