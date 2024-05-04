from .imports import *
from rest_framework.views import APIView
from rest_framework.response import Response
import http.client

class GetOrderBook(APIView):
    def get(self, request):
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

        payload = ''
        # payload_str = json.dumps(payload)
        headers = {
            'Authorization': jwt_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': '192.168.0.102',
            'X-ClientPublicIP': '49.205.145.221',
            'X-MACAddress': '80-38-FB-B9-EE-20',
            'X-PrivateKey': '4dPdQcGs'
        }

        try:
            conn.request("GET", "/rest/secure/angelbroking/order/v1/getOrderBook", payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            print("data:",data)
            return Response(json.loads(data))
            # return Response(data)
        except Exception as e:
            # Handle exceptions
            return Response({"error": str(e)})
