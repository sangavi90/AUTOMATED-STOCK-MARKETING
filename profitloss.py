from .imports import *
from .models import *
import http.client
import json
import pyotp
from rest_framework.views import APIView
from rest_framework.response import Response
from.models import pl,SignInUser
from.serializers import plSerializer

class ProfitLossAPI(APIView):
    def get(self, request):

        legs = Leg.objects.filter(orderstatus='Completed')
        if not legs:
            return Response({"message": "No completed legs found"}, status=status.HTTP_404_NOT_FOUND)

        for leg in legs:
            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                return Response({"error": "Invalid Token: The provided token is not valid."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']
            position_data = smartApi.position()

            if position_data['data']['symbolname'] == leg.name:
                conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
                headers = {
                    'Authorization': jwt_token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-UserType': 'USER',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': '192.168.0.110',
                    'X-ClientPublicIP': '49.205.149.236',
                    'X-MACAddress': '80-38-FB-B9-EE-20',
                    'X-PrivateKey': '4dPdQcGs'
                }

                conn.request("GET", "/rest/secure/angelbroking/portfolio/v1/getAllHolding/",'', headers)
                res = conn.getresponse()
                if res.status == 200:
                    data = json.loads(res.read().decode("utf-8"))
                    for item in position_data['data']:
                        symbolname = item['symbolname']
                        tradingsymbol = item['tradingsymbol']
                        pnl = item['pnl']
                                        
                    # Save the data in the pl model
                    pl_instance = pl.objects.create(
                        company_name=symbolname,
                        trading_symbol=tradingsymbol,
                        profit_loss=pnl
                    )
                    return Response({"message": "Data stored successfully"})
                else:
                    return Response({"error": "Failed to fetch holdings"}, status=res.status)
        
        # If no conditions are met, return a default response
        return Response({"message": "No data processed"})
    
class sendpl(APIView):
    def post(self,request):
        userid=request.data.get('userid')
        print("u= ",userid)
        u=SignInUser.objects.get(user_id=userid)
        print("djndjkvkjv= ",u)
        pandl=pl.objects.filter(user_id=u.pk)
        
        serializer=plSerializer(pandl,many=True)
        print(serializer.data)
        return Response(serializer.data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Leg

class CancelAPI(APIView):
    def post(self, request):
        leg_id = request.data.get("legid")
        func = request.data.get("c_d")
        print(leg_id)

        if not leg_id or not func:
            return Response("Missing legid or c_d parameter", status=status.HTTP_400_BAD_REQUEST)

        try:
            leg = Leg.objects.get(leg_id=leg_id)
        except Leg.DoesNotExist:
            return Response("Leg not found", status=status.HTTP_404_NOT_FOUND)

        if func == "cancel":
            leg.cancel = True
            leg.ltp_status=None
            leg.save()
            return Response("Leg canceled")
        elif func == "delete":
            leg.delete()
            return Response("Leg deleted")
        else:
            return Response("Invalid c_d value", status=status.HTTP_400_BAD_REQUEST)

class DeleteStrategy(APIView):
    def put(self,request):
        strategy_id=request.data.get("strategy_id")
        
        if not strategy_id:
            return Response("Missing strategy_id parameter", status=status.HTTP_400_BAD_REQUEST)

        try:
            strategyid = Strategy.objects.get(strategy_id=strategy_id)
            strategy_name=strategyid.strategy_name
            strategy = Strategy.objects.get(strategy_id=strategy_id)
            strategy.delete()
            return Response({"message":" {} Strategy deleted".format(strategy_name)})
        except Strategy.DoesNotExist:
            return Response("Strategy not found", status=status.HTTP_404_NOT_FOUND)
        


class checkpl(APIView):
    def get(self,request):

            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                return Response({"error": "Invalid Token: The provided token is not valid."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = smartApi.generateSession(username, pwd, totp)
            #return Response(data)
            #jwt_token = data['data']['jwtToken']
            position_data = smartApi.position()
        

            
            positiondata={
                "position_data":position_data,
            }

            profit_and_loss_data = []

            #return Response(dataa)
            user_id="AF44383143346858005933220"
            userr=SignInUser.objects.get(user_id=user_id)
           
            for item in positiondata["position_data"]["data"]:
            # Check if this is the desired tradingsymbol
                if item["tradingsymbol"] == "HINDUNILVR30MAY242280PE":
                    data = {
                        "user_id":userr.pk,
                        "company_name": item["symbolname"],
                        "trading_symbol": item["tradingsymbol"],
                        "profit_loss": item["pnl"]
                    }

                    # Serialize and save the data
                    serializer = plSerializer(data=data)
                    print(serializer)
                    if serializer.is_valid():
                        serializer.save()
                        profit_and_loss_data.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if profit_and_loss_data:
                return Response({"message": "Data saved", "details": positiondata}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No matching trading symbol found"}, status=status.HTTP_404_NOT_FOUND)
