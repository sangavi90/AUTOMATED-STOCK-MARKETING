from django.http import JsonResponse
from rest_framework.views import APIView
from .imports import *
import http.client
from django.http import JsonResponse
from rest_framework.views import APIView
import pyotp

class GetLtpData(APIView):
    def post(self, request):
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
            # print(totp)
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        # correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']
        # print(jwt_token)

        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        payload = """{
            "exchange": "NFO",
            "tradingsymbol": "",
            "symboltoken": "130623"
        }"""

        headers = {
            'Authorization': jwt_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': '192.168.0.108',
            'X-ClientPublicIP': '49.205.145.221',
            'X-MACAddress': '80-38-FB-B9-EE-20',
            'X-PrivateKey': '4dPdQcGs'
        }

        conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", payload, headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        #print(data)

        # Convert the JSON string to a dictionary
        import json
        data_dict = json.loads(data)

        # Return the response in JSON format
        return JsonResponse(data_dict)



class GetLtpData(APIView):
    def check(self, request,exchange,symboltoken):
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
            # print(totp)
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        # correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']
        # print(jwt_token)

        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        payload = {
            "exchange": exchange,
            
            "symboltoken": symboltoken
        }

        headers = {
            'Authorization': jwt_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': '192.168.0.108',
            'X-ClientPublicIP': '49.205.145.221',
            'X-MACAddress': '80-38-FB-B9-EE-20',
            'X-PrivateKey': '4dPdQcGs'
        }

        conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", payload, headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        #print(data)

        # Convert the JSON string to a dictionary
        import json
        data_dict = json.loads(data)

        # Return the response in JSON format
        return JsonResponse(data_dict)
