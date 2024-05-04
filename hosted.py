from django.http import JsonResponse
from rest_framework.views import APIView
from .imports import *
import http.client
from django.http import JsonResponse
from rest_framework.views import APIView
import pyotp
from .models import Leg,SignInUser
import time

from.serializers import plSerializer



from django.http import HttpResponse


##############

# tasks.py


from .models import Leg
import http.client
import json
import pyotp
from .imports import smartApi, username, pwd


####################################################

class ExitOnTrigger(APIView):
    def post(self,request):
        orderid = request.data.get('orderid')
        user_id=request.data.get("userid")
        print("class ExitOntrigger=", orderid)
        
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            headers = {
                'Authorization': jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '62.72.59.145:9000',
                'X-ClientPublicIP': '49.205.147.203',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-PrivateKey': '4dPdQcGs'
            }

            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            leg = Leg.objects.get(orderid=orderid)

            exit_trigger_params = {
                "variety": leg.variety,
                "tradingsymbol": leg.tradingsymbol,
                "symboltoken": leg.symboltoken,
                "transactiontype": "SELL" if leg.transactiontype.upper() == "BUY" else "BUY",
                "exchange": leg.exchange,
                "ordertype": leg.ordertype,
                "producttype": leg.producttype,
                "duration": leg.duration,
                "price": "0",
                "squareoff": "0",
                "stoploss": "0",
                "quantity": leg.quantity,
                "orderid":leg.orderid
            }

            leg.triggerstatus="matching.."
            leg.save()
            
            ############################# Below code is for Call option ####################################
            while leg.optiontype.upper()=="CE":
                leg = Leg.objects.get(orderid=orderid)

                if leg.stoplossstatus=="stoploss executed":
                    return Response("Stoploss executed ")
                
                print("checking to trigger")
                payloads = {
                    "exchange": "NSE",
                    "symboltoken": leg.nse_symboltoken
                }
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                spotprice = data_dict['data']['ltp']
                print("trigeer spotprice= ",spotprice)
                print("leg.triggerprice= ",leg.triggerprice)

                                             
                if  spotprice >= float(leg.triggerprice):  
                    #order_id = smartApi.placeOrder(exit_trigger_params)

                    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(exit_trigger_params), headers)

                    leg.triggerstatus = 'trigger executed'
                    leg.stoplossstatus = "stoploss not executed"
                    leg.ltp_status="completed"
                    leg.save()

                    position_data = smartApi.position()
            
                    positiondata={
                        "position_data":position_data,
                    }
                    userr=SignInUser.objects.get(user_id=user_id)                                   
                    for item in positiondata["position_data"]["data"]:
                    # Check if this is the desired tradingsymbol
                        
                        if item["tradingsymbol"] == leg.tradingsymbol:
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
                                
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            
                    return Response("Exit trigger order placed successfully")

                # Check if stop flag is set
                
                # if leg.stop_trigger_flag:
                #     print("doneeee")
                #     return Response("Trigger stopped")

                time.sleep(1)  # Adjust delay as needed

            ########################## Below code is for Put option ################################

            while leg.optiontype.upper()=="PE":
                leg = Leg.objects.get(orderid=orderid)

                if leg.stoplossstatus=="stoploss executed":
                    return Response("Stoploss executed ")
                
                print("checking to trigger")
                payloads = {
                    "exchange": "NSE",
                    "symboltoken": leg.nse_symboltoken
                }
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                spotprice = data_dict['data']['ltp']
                print("trigeer spotprice= ",spotprice)
                print("leg.triggerprice= ",leg.triggerprice)

                                             
                if  spotprice <= float(leg.triggerprice):  
                    #order_id = smartApi.placeOrder(exit_trigger_params)

                    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(exit_trigger_params), headers)

                    leg.triggerstatus = 'trigger executed'
                    leg.stoplossstatus = "stoploss not executed"
                    leg.ltp_status="completed"
                    leg.save()

                    position_data = smartApi.position()
            
                    positiondata={
                        "position_data":position_data,
                    }
                    userr=SignInUser.objects.get(user_id=user_id)                                   
                    for item in positiondata["position_data"]["data"]:
                    # Check if this is the desired tradingsymbol
                        
                        if item["tradingsymbol"] == leg.tradingsymbol:
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
                                
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            
                    return Response("Exit trigger order placed successfully")

                # Check if stop flag is set
                
                # if leg.stop_trigger_flag:
                #     print("doneeee")
                #     return Response("Trigger stopped")

                time.sleep(1)  # Adjust delay as needed

        except Exception as e:
            logger.error(f"Error: {e}")
            return Response("An error occurred while processing the request", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #return Response("LTP checked and trigger not met")

    
###########################################################
class ExitOnstoploss(APIView):
    def post(self, request):
        orderid = request.data.get('orderid')
        user_id=request.data.get('userid')

        
        print("class ExitOnstoploss=", orderid)

        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            headers = {
                'Authorization': jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '62.72.59.145',
                'X-ClientPublicIP': '49.205.147.203',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-PrivateKey': '4dPdQcGs'
            }

            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            leg = Leg.objects.get(orderid=orderid)

            payloads = {
                    "exchange": "NSE",
                    "symboltoken": leg.nse_symboltoken
                }
            conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            data_dict = json.loads(data)

            CEstored_spotprice = data_dict['data']['ltp']
            PEstored_spotprice = data_dict['data']['ltp']

            exit_trigger_params = {
                "variety": leg.variety,
                "tradingsymbol": leg.tradingsymbol,
                "symboltoken": leg.symboltoken,
                "transactiontype": "SELL" if leg.transactiontype.upper() == "BUY" else "BUY",
                "exchange": leg.exchange,
                "ordertype": leg.ordertype,
                "producttype": leg.producttype,
                "duration": leg.duration,
                "price": "0",
                "squareoff": "0",
                "stoploss": "0",
                "quantity": leg.quantity,
                #"orderid":leg.orderid
            }

            print(exit_trigger_params)
            leg.stoplossstatus="matching.."
            leg.save()

            ######### BELOW CODE IS FOR CE ##################
            while leg.optiontype.upper()=="CE":
                leg = Leg.objects.get(orderid=orderid)
                

                if leg.triggerstatus=="trigger executed":
                    return Response(" trigger price executed ")
                
                payloads = {
                    "exchange": "NSE",
                    "symboltoken": leg.nse_symboltoken
                }
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                spotprice = data_dict['data']['ltp']

                # Update stop loss if the current price equals current price plus trailing stop loss:
                print("real spot price= ",spotprice)
                print("CEstored_spotprice= ",CEstored_spotprice)
                
                print("leg.stoploss= ",leg.stoploss)

                # if float(spotprice)>=(float(stored_spotprice)+float(leg.trailingstoploss)):
                #     leg.stoploss=str(float(leg.stoploss)+float(leg.trailingstoploss))
                #     stored_spotprice=spotprice
                #     leg.save()

                if float(spotprice)-float(CEstored_spotprice)>=float(leg.trailingstoploss):
                    print("updating =",float(leg.stoploss))
                    print("trailing= ",float(leg.trailingstoploss))
                    leg.stoploss=str(round(float(leg.stoploss)+float(leg.trailingstoploss),1))
                    CEstored_spotprice=spotprice
                    leg.save()

                       
                if float(leg.stoploss) == spotprice:
                    #order_id = smartApi.placeOrder(exit_trigger_params)

                    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(exit_trigger_params), headers)


                    leg.stoplossstatus = 'stoploss executed'
                    leg.triggerstatus="triggerstatus not executed"
                    leg.ltp_status="completed"
                    leg.save()

                    position_data = smartApi.position()
            
                    positiondata={
                        "position_data":position_data,
                    }
                    userr=SignInUser.objects.get(user_id=user_id)                                
                    for item in positiondata["position_data"]["data"]:
                    # Check if this is the desired tradingsymbol
                        
                        if item["tradingsymbol"] == leg.tradingsymbol:
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
                                
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            

                    return Response("Exit trigger order placed successfully")

                # Check if stop flag is set
                
                # if leg.stop_trigger_flag:
                #     print("doneeee")
                #     return Response("Trigger stopped")

                time.sleep(1)  # Adjust delay as needed
            ################### BELOW CODE IS FOR PUT OPTION  ###################################
            while leg.optiontype.upper()=="PE":
                leg = Leg.objects.get(orderid=orderid)
                

                if leg.triggerstatus=="trigger executed":
                    return Response(" trigger price executed ")
                
                payloads = {
                    "exchange": "NSE",
                    "symboltoken": leg.nse_symboltoken
                }
                conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                data_dict = json.loads(data)

                spotprice = data_dict['data']['ltp']

                # Update stop loss if the current price equals current price plus trailing stop loss:
                #print("real spot price= ",spotprice)
                #print("PEstored_spotprice= ",PEstored_spotprice)
                
                #print("leg.stoploss= ",leg.stoploss)

                # if float(spotprice)>=(float(stored_spotprice)+float(leg.trailingstoploss)):
                #     leg.stoploss=str(float(leg.stoploss)+float(leg.trailingstoploss))
                #     stored_spotprice=spotprice
                #     leg.save()

                if float(PEstored_spotprice)-float(spotprice)>=float(leg.trailingstoploss):
                    print("updating =",float(leg.stoploss))
                    print("trailing= ",float(leg.trailingstoploss))
                    leg.stoploss=str(round(float(leg.stoploss)-float(leg.trailingstoploss),1))
                    PEstored_spotprice=spotprice
                    leg.save()

                       
                if float(leg.stoploss) == spotprice:
                    #order_id = smartApi.placeOrder(exit_trigger_params)

                    conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(exit_trigger_params), headers)


                    leg.stoplossstatus = 'stoploss executed'
                    leg.triggerstatus="triggerstatus not executed"
                    leg.ltp_status="completed"
                    leg.save()

                    position_data = smartApi.position()
            
                    positiondata={
                        "position_data":position_data,
                    }
                    userr=SignInUser.objects.get(user_id=user_id)                               
                    for item in positiondata["position_data"]["data"]:
                    # Check if this is the desired tradingsymbol
                        
                        if item["tradingsymbol"] == leg.tradingsymbol:
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
                                
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            

                    return Response("Exit trigger order placed successfully")

                # Check if stop flag is set
                
                # if leg.stop_trigger_flag:
                #     print("doneeee")
                #     return Response("Trigger stopped")

                time.sleep(1)  # Adjust delay as needed

        except Exception as e:
            logger.error(f"Error: {e}")
            return Response("An error occurred while processing the request", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #return Response("LTP checked and trigger not met")

   


####################################################



class OrderOnprice(APIView):
    def post(self, request):
        legid = request.data.get('leg_id')
        
        print("legId is =",legid)
        

        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            headers = {
                'Authorization': jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '62.72.59.145',
                'X-ClientPublicIP': '49.205.147.203',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-PrivateKey': '4dPdQcGs'
            }

            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            leg = Leg.objects.get(leg_id=legid)

            order_on_params = {
                

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
                            #"stoploss": "",
                            "quantity": str(leg.quantity),
                            #"triggerprice": "",
                            "expirydate": leg.expirydate,
                            "strikeprice": leg.strikeprice,
                            "instrumenttype":"OPTSTK", #newl added fields
                            "optiontype":leg.optiontype.upper(),
            }

            leg.cancel=False
            leg.ltp_status="matching.."
            leg.save()
            

            while True:
                  leg = Leg.objects.get(leg_id=legid,ltp_status="matching..")
                  print("legId is =",legid)
                  #print(leg.cancel)
                  if leg.cancel==True:
                      
                      break

                  print("checking")
                  payloads = {
                      "exchange": "NSE",
                      "symboltoken": leg.nse_symboltoken
                  }
                  
                  conn.request("POST", "/rest/secure/angelbroking/order/v1/getLtpData", json.dumps(payloads), headers)
                  res = conn.getresponse()
                  data = res.read().decode("utf-8")
                  data_dict = json.loads(data)

                  spotprice = data_dict['data']['ltp']
                  print("spotprice= ",spotprice)
                  print("leg.price= ",leg.price)

                  

                  
                  if float(leg.price) == float(spotprice):
                      #order_id = smartApi.placeOrder(order_on_params)

                      conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(order_on_params), headers)
                      res = conn.getresponse()

                      data = res.read().decode("utf-8")

                      print(json.loads(data))

                      leg.orderid=json.loads(data)['data']['orderid']

                      leg.uniqueorderid=json.loads(data)['data']["uniqueorderid"]
                      unique=json.loads(data)['data']["uniqueorderid"]
                      #leg.triggerstatus="matching.."

                      #leg.stoplossstatus="matching.."

                      conn.request("GET", "/rest/secure/angelbroking/order/v1/details/" + unique, "", headers)

                      ress = conn.getresponse()
                      dataa = ress.read().decode("utf-8")
                      print("data:",json.loads(dataa)['data']['orderstatus'])

                      


                      #leg.ltp_status = json.loads(dataa)['data']['orderstatus']
                      leg.ltp_status="executed"
                      leg.save()

                      return Response("Order executed successfully")
                    

                  time.sleep(1)  # Adjust delay as needed

        except Exception as e:
           
            leg.ltp_status=None
            leg.save()
            print(e)
            
            return Response("An error occurred while running", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("LTP checked and trigger not met")

    

          
        

############################################

class ExitwhereItis(APIView):
    def post(self, request):
        orderid = request.data.get('orderid')
        user_id=request.data.get("user_id")
        
        print(orderid)

        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            headers = {
                'Authorization': jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '62.72.59.145',
                'X-ClientPublicIP': '62.72.59.145',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-PrivateKey': '4dPdQcGs'
            }

            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            leg = Leg.objects.get(orderid=orderid)

            order_on_params = {
                

                            "variety": leg.variety,
                            "tradingsymbol": leg.tradingsymbol,
                            "symboltoken": leg.symboltoken,
                            "transactiontype": "SELL" if leg.transactiontype.upper() == "BUY" else "BUY",
                            "exchange":leg.exchange,
                            "ordertype":leg.ordertype,
                            "producttype": leg.producttype,
                            "duration": leg.duration,                            
                            "squareoff": '0',                           
                            "quantity": str(leg.quantity),                           
                            "expirydate": leg.expirydate,
                            "strikeprice": leg.strikeprice,
                            "instrumenttype":"OPTSTK", #newl added fields
                            "optiontype":leg.optiontype.upper(),
            }

            print(order_on_params)
            while True:
                print("checking")
                

                conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(order_on_params), headers)
                res = conn.getresponse()
                
                data = res.read().decode("utf-8")
                
                print(json.loads(data))
                
                unique=json.loads(data)['data']["uniqueorderid"]
                conn.request("GET", "/rest/secure/angelbroking/order/v1/details/" + unique, "", headers)

                res = conn.getresponse()
                dataa = res.read().decode("utf-8")
                print("data:",json.loads(dataa)['data']['orderstatus'])
                    
                    

                leg.exitwhereitis="exited on spot price" 
                #leg.ltp_status=json.loads(dataa)['data']['orderstatus']  
                leg.ltp_status="completed" 
                leg.stoplossstatus=None
                leg.triggerstatus=None
                leg.save()

                position_data = smartApi.position()
            
                positiondata={
                    "position_data":position_data,
                }
                userr=SignInUser.objects.get(user_id=user_id)                              
                for item in positiondata["position_data"]["data"]:
                # Check if this is the desired tradingsymbol
                    
                    if item["tradingsymbol"] == leg.tradingsymbol:
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
                            
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        
                time.sleep(1)

                return Response("order exited successfully based on spot price")

                

                #time.sleep(1)  # Adjust delay as needed

        except Exception as e:
            logger.error(f"Error: {e}")
            return Response("An error occurred while processing the request", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("LTP checked and trigger not met")

################################################
