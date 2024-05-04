
from .imports import *
from .models import *

from .serializers import *
api_key = '4dPdQcGs'
username = 'S2098754'
pwd = '2024'
smartApi = SmartConnect(api_key)
XClientLocalIP='192.168.0.103'

class get_details(APIView):
    def get(self,request):

        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
            print(totp)
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        # correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']
        print(jwt_token)
        return Response(data)   


class get_trade_book(APIView):
    def get(self,request):
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
            print(totp)
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        # correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']

        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            
            
        payload = "{\n\"clientcode\":\"S2098754\",\n\"password\":\"]2024\"\n,\n\"totp\":\"AFH6577WNNSGC4TGXVLJWHVAQI\"\n}"
        headers = {
        'Authorization': jwt_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': '192.168.0.103',
        'X-ClientPublicIP': '49.205.145.221',
        'X-MACAddress': MACAddress,
        'X-PrivateKey': api_key
        }
        conn.request("GET","/rest/secure/angelbroking/order/v1/getTradeBook",payload,headers)
        

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

        return Response(data)
    
#  Program get trade book using smart api:
class get_order_book(APIView):
    def get(self,request):
        import http.client

        conn = http.client.HTTPSConnection(
            "apiconnect.angelbroking.com"
            )
        payload = '''{\n 
            \"exchange\": \"NSE\",
            \n    \"tradingsymbol\": \"INFY-EQ\",
            \n    \"quantity\": 5,
            \n    \"disclosedquantity\": 3,
            \n    \"transactiontype\": \"BUY\",
            \n    \"ordertype\": \"MARKET\",
            \n    \"variety\": \"STOPLOSS\",
            \n    \"producttype\": \"INTRADAY\"
            \n}'''
        headers = {
        'Authorization': 'Bearer AUTHORIZATION_TOKEN',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': '192.168.0.103',
        'X-ClientPublicIP': "49.205.145.221",
        'X-MACAddress': 'MAC_ADDRESS',
        'X-PrivateKey': 'API_KEY'
        }
        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", 
        payload, 
        headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))


#  Get the real time data by using Smart Api code:
 
class real_time_data(APIView):
    def get(self,request):



        api_url = 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/market/v1/quote/'

        # Define your API key and other necessary headers
        headers = {
            'X-PrivateKey': api_key,
            'Authorization': jwt_token,
            'Content-Type': 'application/json'
        }

        # Define the payload (optional)
        payload = {
            "mode": "FULL",
            "exchangeTokens": {
                 "NSE": ["3045"]
        }

        
        }

        # Make a POST request to the API endpoint
        response = requests.post(api_url, json=payload, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract and process the real-time market data from the response
            market_data = response.json()
            print(market_data)
        else:
            # Print an error message if the request failed
            print("Failed to retrieve real-time market data. Status code:", response.status_code)

        return Response(market_data)



#  Based on NIFTY and Expiry-date it shows all the details of CE and PE: 

class NSE_real_time_data(APIView):
    def get(self,request):
        url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response=requests.get(url,headers=headers)
        print(response)


        response_text=response.text
        print(response_text)
        json_object=json.loads(response_text)
        # print(type(json_object))
        
        return Response(json_object)
        
#  it display only Strike_price of CE,PE:
    
class NSE_option_chain_data_check(APIView):
    def get(self,request,symbol):
        url='https://www.nseindia.com/api/option-chain-equities?symbol={}'.format(symbol)
        print(url)
        print("jhvjgfjgjg=",symbol)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        response=requests.get(url,headers=headers)
        


        response_text=response.text
        # print(response_text)
        json_object=json.loads(response_text)
        # print(json_object)
        ce_strike_prices = []
        pe_strike_prices = []
        
        for data in json_object['records']['data']:
            if 'CE' in data:
                ce_strike_prices.append(data['CE']['strikePrice'])
            if 'PE' in data:
                pe_strike_prices.append(data['PE']['strikePrice'])
        
        data= {
            'CE': ce_strike_prices,
            'PE': pe_strike_prices
        }
    
        return Response(data)
 
# it display all the company name only ,which are all take it from OI_Spruts:

class NSE_company_name(APIView):
     def get(self,request):
         companies = company_name.objects.all()
         
        
        #  serializer = CompanyNameSerializer(com_name, many=True)
         data=[i.company_name for i in companies]
        
         return Response(data)
     

# It stores all the company name into database:

class NSE_option_chain_data(APIView):
    def get(self, request):
        companies = company_name.objects.all()
        i = 0
        for company in companies:
            symbol = company.company_name
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol={}'.format(symbol)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                json_object = response.json()

                ce_strike_prices = []
                pe_strike_prices = []

                for data in json_object['records']['data']:
                    if 'CE' in data:
                        ce_strike_prices.append(data['CE']['strikePrice'])
                    if 'PE' in data:
                        pe_strike_prices.append(data['PE']['strikePrice'])

                # Check if options entry already exists for the company
                existing_options = options.objects.filter(company_name=company)
                if existing_options.exists():
                    print(company.company_name, "already exists")
                    continue

                # Create or update options instance
                options.objects.create(
                    company_name=company,
                    ce=ce_strike_prices,
                    pe=pe_strike_prices
                )
                i += 1
                print(company.company_name, " ", i)
            else:
                print(company.company_name, " not appended ")
        c = options.objects.all().count()
        print("total companies = ", c)
        return JsonResponse({'message': 'Data saved successfully'})
    

#  Based on company name it display Strike_price of CE and PE:

import ast
class OptionsData(APIView):
    def get(self, request, symbol):
        try:
            # Retrieve options data for the provided company name
            company = company_name.objects.get(company_name=symbol)
            options_data = options.objects.get(company_name=company)

            # Serialize the CE and PE values
            serializer = OptionsSerializer(options_data)
            ce_list = ast.literal_eval(serializer.data['ce'])
            pe_list = ast.literal_eval(serializer.data['pe'])
            data={
                'company_name':symbol,
                'ce':ce_list,
                'pe':pe_list
            }
            return Response(data)
        except company_name.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        except options.DoesNotExist:
            return Response({'error': 'Options data not found for the company'}, status=404)    
        
class Order_placing(APIView):
    def get(self, request):
        try:
            # Generate TOTP
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()

            # Generate session
            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            # Prepare payload for placing order
            payload = {
                "exchange": "NSE",
                "tradingsymbol": "INFY-EQ",
                "quantity": 5,
                "disclosedquantity": 3,
                "transactiontype": "BUY",
                "ordertype": "MARKET",
                "variety": "STOPLOSS",
                "producttype": "INTRADAY"
            }

            # Make request to place order
            headers = {
                'Authorization': jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '192.168.0.103',
                'X-ClientPublicIP': '49.205.145.221',
                'X-MACAddress': MACAddress,
                'X-PrivateKey': api_key
            }
            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", json.dumps(payload), headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            # Close connection
            conn.close()

            return Response(data)
        except Exception as e:
            logger.error("Error placing order: {}".format(str(e)))
            return Response("Error placing order: {}".format(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpiryStrikePrice(APIView):
    def get(self, request, symbol):
        companies = company_name.objects.all()
        error_companies = []

        for company in companies:
            symbol = company.company_name
            url = 'https://www.nseindia.com/api/option-chain-equities?symbol={}'.format(symbol)
            print(url)
            print("Company:", symbol)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
            
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for bad responses (e.g., 404, 500)
                json_object = response.json()

                ce_options = []
                pe_options = []

                for data in json_object['records']['data']:
                    if 'CE' in data:
                        ce_option = {
                            'expiry_date': data['expiryDate'],
                            'strike_price': data['CE']['strikePrice']
                        }
                        ce_options.append(ce_option)
                    if 'PE' in data:
                        pe_option = {
                            'expiry_date': data['expiryDate'],
                            'strike_price': data['PE']['strikePrice']
                        }
                        pe_options.append(pe_option)

                data = {
                    'CE': ce_options,
                    'PE': pe_options
                }

                existing_options = expirystrikeprice.objects.filter(company_name=company)
                if existing_options.exists():
                    print(company.company_name, "already exists")
                    continue

                expirystrikeprice.objects.create(
                    company_name=company,
                    ce=ce_options,
                    pe=pe_options)

                print(len(data))
                return Response(data)

            except (requests.RequestException, json.JSONDecodeError) as e:
                print(f"Error processing {symbol}: {e}")
                error_companies.append(symbol)
                print(error_companies) 
                print(len(error_companies))
                continue
        
        return Response({"error_companies": error_companies})



 # Based on company name it shows collection of Expiry-date and Strike price of CE and PE: 
    
import ast
class ExpiryStrikeData(APIView):      # this API for display expiry date , strike_price with their  company_name.
    def get(self, request, symbol):
        try:
            # Retrieve options data for the provided company name
            company = company_name.objects.get(company_name=symbol)
            options_data =expirystrikeprice.objects.get(company_name=company)

            # Serialize the CE and PE values
            serializer =ExpiryPriceSerializer(options_data)
            ce_list = ast.literal_eval(serializer.data['ce'])
            pe_list = ast.literal_eval(serializer.data['pe'])
            data={
                'company_name':symbol,
                'ce':ce_list,
                'pe':pe_list
            }
            return Response(data)
        except company_name.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        except expirystrikeprice.DoesNotExist:
            return Response({'error': 'Options data not found for the company'}, status=404)   


#  based on Expiry-date it shows collecction of Stike_price of CE and PE:

class based_on_expiry_date(APIView): 
    def get(self, request, symbol):
        try:
            url = f'https://www.nseindia.com/api/option-chain-equities?symbol={symbol}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers)
            response_json = response.json()

            ce_options = {}
            pe_options = {}

            for data in response_json['records']['data']:
                expiry_date = data['expiryDate']

                # CE (Call Option) strike price
                if 'CE' in data:
                    ce_strike_price = data['CE']['strikePrice']
                    if expiry_date not in ce_options:
                        ce_options[expiry_date] = []
                    ce_options[expiry_date].append(ce_strike_price)

                # PE (Put Option) strike price
                if 'PE' in data:
                    pe_strike_price = data['PE']['strikePrice']
                    if expiry_date not in pe_options:
                        pe_options[expiry_date] = []
                    pe_options[expiry_date].append(pe_strike_price)

            result = {
                'CE': ce_options,
                'PE': pe_options
            }

            return Response(result)
        
        except Exception as e:
            return Response({'error': str(e)})



class Tradingsymbol_token(APIView):
    def get(self, request):
        # Fetch data from the URL
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Filter data for symbols ending with "-EQ", exch_seg="NSE", and specific names
            filtered_data = [item for item in data if item.get('exch_seg', '') == "NSE"  if item.get('symbol', '').endswith("-EQ") 
                             or item.get('name', '') in ["NIFTY", "FINNIFTY", "BANKNIFTY", "MIDCPNIFTY"]]
            
            if filtered_data:
                # Extract name, trading_symbol, and token for filtered data
                extracted_data = [{'name': item['name'], 'trading_symbol': item['symbol'], 'token': item['token']} for item in filtered_data]
                print("djfbhdfdkfdfd=",len(extracted_data))
                j=0
                for i in extracted_data:
                    j+=1
                    if i['name']=="NIFTY"or i['name']=="FINNIFTY" or i['name']=="BANKNIFTY" or i['name']=="MIDCPNIFTY" :
                        print("yes",i['name'],"   ",i['trading_symbol'],"   ",i['token'])
                        
                        
                print("count of al companies are =",j)
                return Response(extracted_data)
                
            else:
                return Response({"error": "No symbols found ending with '-EQ' for exch_seg='NSE' and specified names"}, status=404)
        else:
            # If there's an error fetching the data
            return Response({"error": "Failed to fetch data from the URL"}, status=response.status_code)
    


        


import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import company_name# Import your CompanyName model

class NSE_Tradingsymbol_token(APIView):
    def get(self, request):
        # Fetch data from the URL
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Get company names from the model
            company_names = company_name.objects.values_list('company_name', flat=True)
            
            data = response.json()
            
            # Initialize an empty list to store matched data
            matched_data_list = []
            
            # Iterate over each item in the JSON data
            for item in data:
                # Check if the company name from the model matches the 'name' attribute in the JSON data
                if item.get('name', '') in company_names and item.get('symbol', '').endswith("-EQ"):
                    # If there's a match, extract the required data
                    matched_data = {
                        'name': item['name'],
                        'symbol': item['symbol'],
                        'token': item['token']
                    }
                    matched_data_list.append(matched_data)
            
            # Check if any data was matched
            if matched_data_list:
                return Response(matched_data_list)
            else:
                return Response({"error": "No matching data found"}, status=404)
        else:
            # If there's an error fetching the data
            return Response({"error": "Failed to fetch data from the URL"}, status=response.status_code)
        
from .models import Strategy
from .serializers import StrategySerializer
####################################### store the Strategy and leg in database by getting user_id and strategy:#####################################
class StrategyView(APIView):  
    def post(self, request):

        print(request.data)

        user_id=request.data.get('user_id')
        strategy_name=request.data.get('strategy_name')
        

        user=SignInUser.objects.get(user_id=user_id)
        serializer_data = {
            'user_id': user.pk, 
            'strategy_name': strategy_name
            
        }
        
        strategy_serializer = StrategySerializer(data=serializer_data)
        print(strategy_serializer)
        if strategy_serializer.is_valid():
            strategy_instance = strategy_serializer.save()

            leg_data = request.data.get('leg', [])
            print("data is=",leg_data)
            legs_to_create = []
            for leg in leg_data:
                leg['strategy_name'] = strategy_instance.id  # Associate leg with the created strategy

                print("jdbhjbdc= ",leg['name'])
                sym=company_name.objects.get(company_name=leg['name'])
                print("company symboltoken is = ",sym.symboltoken)
                leg['nse_symboltoken']=sym.symboltoken
                
                leg_serializer = LegSerializer(data=leg)
                if leg_serializer.is_valid():
                    legs_to_create.append(leg_serializer.save())
                else:
                    return Response(leg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Strategy and Legs created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(strategy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Strategy, Leg
#######################################based on strategy name it sends all leg details:##############################
class RetrieveLegFields(APIView):
    def get(self, request):
        # Retrieve all strategies from the database
        strategies = Strategy.objects.all()

        data_list = []
        for strategy in strategies:
            # Retrieve all legs associated with the current strategy
            legs = Leg.objects.filter(strategy_name=strategy)
            
            # Prepare leg data for the current strategy
            leg_data_list = []
            for leg in legs:
                leg_data = {
                    "variety": leg.variety,
                    "tradingsymbol": leg.tradingsymbol,
                    "symboltoken": leg.symboltoken,
                    "transactiontype": leg.transactiontype,
                    "exchange": leg.exchange,
                    "ordertype": leg.ordertype,
                    "producttype": leg.producttype,
                    "duration": leg.duration,
                    "price": leg.price,
                    "stoploss": leg.stoploss,
                    "quantity": leg.quantity,
                    "triggerprice": leg.triggerprice,
                    "expirydate": leg.expirydate,
                    "strikeprice": leg.strikeprice,
                    "totallot": leg.totallot,
                    "trailingstoploss": leg.trailingstoploss
                }
                leg_data_list.append(leg_data)

            # Prepare data for the current strategy
            strategy_data = {
                "strategy_name": strategy.strategy_name,
                "legs": leg_data_list
            }
            data_list.append(strategy_data)

        return Response(data_list, status=status.HTTP_200_OK)
    
    from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Strategy
from .serializers import StrategySerializer


        
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Strategy, Leg
from .serializers import StrategySerializer, LegSerializer
####################################based on  user_id it sends all the strategy and also legs under the strategy#################################
class RetrieveStrategyByUserId(APIView):
    def post(self, request):
        try:
            # Get user_id from request data
            user_id = request.data.get('user_id')
            
            # Retrieve strategies associated with the user_id
            user=SignInUser.objects.get(user_id=user_id)
            strategies = Strategy.objects.filter(user_id=user.pk)
            
            
            # Serialize the strategies
            strategy_data = []
            for strategy in strategies:
                strategy_serializer = StrategySerializer(strategy)
                strategy_data.append(strategy_serializer.data)
                
                # Retrieve legs associated with the strategy
                legs = Leg.objects.filter(strategy_name=strategy)
                leg_serializer = LegSerializer(legs, many=True)
                
                # Add legs data to the serialized strategy data
                strategy_data[-1]['legs'] = leg_serializer.data
            
            # Return serialized data
            return Response(strategy_data, status=status.HTTP_200_OK)
        
        except Strategy.DoesNotExist:
            return Response({'message': 'No strategies found for the provided user_id'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class user_details(APIView):
    def post(self,request):

        user_id=request.data.get('user_id')
        user=SignInUser.objects.get(user_id=user_id)
        serializer = SignInUserSerializer(user)

        return Response({'message': 'Login successful', 'user': serializer.data})

############# based on status="active" order get place and also store unique order id in leg database:##########################
class status_view(APIView):
    def post(self,request):
        user_id=request.data.get('user_id')
        strategy_id=request.data.get('strategy_id')
        stat=request.data.get('status')
        print('status is= ',request.data)
        user=SignInUser.objects.get(user_id=user_id)
        status=Strategy.objects.get(user_id=user.pk,strategy_id=strategy_id)
        status.status=stat
        status.save()

        try:
            username = 'S2098754'
            pwd = '2024'
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        # Get orders from the request dataorders = request.data.get("orders", [])
       
        response_data = []
        order_data= []
       
        try:
                
                # Extracting required fields from the order
                # strategy_id='STAF7D6264'
                # Check if strategy is active before placing order
                if Strategy.objects.filter(strategy_id=strategy_id, status='active').exists():
                    # Fetch strategy associated with the order
                    strategy = Strategy.objects.get(strategy_id=strategy_id)
                    # Fetch legs associated with the strategy
                    legs = Leg.objects.filter(strategy_name=strategy)
                    print(legs)
                    # Iterate over the legs
                    i=0
                    for leg in legs:

                        
                        # Construct the payload for the order
                        print(leg.variety)

                        payload = {
                            "variety": leg.variety,
                            "tradingsymbol": leg.tradingsymbol,
                            "symboltoken": leg.symboltoken,
                            "transactiontype": leg.transactiontype.upper(),
                            "exchange":leg.exchange,
                            "ordertype":leg.ordertype,
                            "producttype": leg.producttype,
                            "duration": leg.duration,
                            "price": leg.price,
                            "squareoff": '0',
                            "stoploss": leg.stoploss,
                            "quantity": str(leg.quantity),
                            "triggerprice": leg.triggerprice,
                            "expirydate": leg.expirydate,
                            "strikeprice": leg.strikeprice
                        }

                        payload_str = json.dumps(payload)
                        print("payload str= ",payload_str)
                        headers = {
                            'Authorization': jwt_token,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'X-UserType': 'USER',
                            'X-SourceID': 'WEB',
                            'X-ClientLocalIP': '192.168.0.103',
                            'X-ClientPublicIP': '49.205.145.221',
                            'X-MACAddress': '80-38-FB-B9-EE-20',
                            'X-PrivateKey': '4dPdQcGs'
                        }
                        # print(headers)
                             # Place the order using the payload
                        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
                        res = conn.getresponse()

                        print(type(res))
                        print("res",res)
                        
                        data = res.read().decode("utf-8")
                        # response_data.append(data)
                        # return Response.append(data)
                        
                        #print("Response data:",data)
                        # print(json.loads(data))
                        response_data.append(json.loads(data))
                        orderid = response_data[i]["data"]["orderid"]
                        uniqueorderid = response_data[i]["data"]["uniqueorderid"]
                        i+=1

                        print("Order ID:", orderid)
                        print("Unique Order ID:", uniqueorderid)

                        leg.orderid=orderid
                        leg.uniqueorderid=uniqueorderid
                        leg.save()

                        conn.request("GET", "/rest/secure/angelbroking/order/v1/details/" + uniqueorderid, "", headers)

                        res = conn.getresponse()
                        o_data = res.read().decode("utf-8")
                        

                        order_data.append({
                            'message': 'Order placed successfully',
                            'uniqueorderid': uniqueorderid,
                            "order_data":json.loads(o_data)
                            })
                else:
                     # Handle HTTP errors
                     print("HTTP Error:", res.status)
                     response_data.append({"error": "HTTP Error: " + str(res.status)})
                    # response_data.append({"error": "Strategy is not active, order not placed"})
        except Exception as e:
                # Handle exceptions for individual orders if needed
                print('nnnnnnnnnnnnnnnnnnnnn',e)
                response_data.append({"error": str(e)})

        

        print("response",response_data)
        return Response(order_data)
        # return Response({'status':stat})





from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Strategy, Leg
from .serializers import StrategySerializer, LegSerializer
from .serializers import StrategySerializer
#if status active then only order get place :
class MultipleLegs(APIView):
    def post(self, request):
        print(request.data)
        strategy_id=request.data.get('strategy_id')
        try:
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        data = smartApi.generateSession(username, pwd, totp)
        jwt_token = data['data']['jwtToken']
        conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

        # Get orders from the request data
        # orders = request.data.get("orders", [])
        # print(orders)
        response_data = []
        # for order in orders:
        try:
                # Extracting required fields from the order
                # strategy_id = order.get("strategy_id")

                # Check if strategy is active before placing order
                if Strategy.objects.filter(strategy_id=strategy_id, status='active').exists():
                    # Fetch strategy associated with the order
                    strategy = Strategy.objects.get(strategy_id=strategy_id)
                    # Fetch legs associated with the strategy
                    legs = Leg.objects.filter(strategy_name=strategy)

                    # Iterate over the legs
                    for leg in legs:
                        # Construct the payload for the order
                        payload = {
                            "variety": leg.variety,
                            "tradingsymbol": leg.tradingsymbol,
                            "symboltoken": leg.symboltoken,
                            "transactiontype": leg.transactiontype,
                            "exchange": leg.exchange,
                            "ordertype": leg.ordertype,
                            "producttype": leg.producttype,
                            "duration": leg.duration,
                            "price": leg.price,
                            "squareoff": "0",
                            "stoploss": leg.stoploss,
                            "quantity": leg.quantity,
                            "triggerprice": leg.triggerprice,
                            "expirydate": leg.expirydate,
                            "strikeprice": leg.strikeprice
                        }

                        print(payload_str)

                        payload_str = json.dumps(payload)
                        headers = {
                            'Authorization': jwt_token,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'X-UserType': 'USER',
                            'X-SourceID': 'WEB',
                            'X-ClientLocalIP': '192.168.0.103',
                            'X-ClientPublicIP': '49.205.145.221',
                            'X-MACAddress': '80-38-FB-B9-EE-20',
                            'X-PrivateKey': '4dPdQcGs'
                        }

                        # Place the order using the payload
                        conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", payload_str, headers)
                        res = conn.getresponse()
                        data = res.read().decode("utf-8")
                        response_data.append(json.loads(data))
                else:
                    response_data.append({"error": "Strategy is not active, order not placed"})
        except Exception as e:
                # Handle exceptions for individual orders if needed
                response_data.append({"error": str(e)})
        print(response_data)
        return Response(response_data)






#########################################SIGNIN ,LOGIN,FORGOT PASSWORD#################################################
# from .models import SignInUser

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.hashers import make_password, check_password
# from .models import SignInUser

# class SignInUserAPIView(APIView):
#     def post(self, request):
#         # Extract data from the request
#         print(request.data)
#         print("hi")
#         username = request.data.get('username')
#         email = request.data.get('email')
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')
#         request.session['username']=username
#         # Check if the user already exists
#         if SignInUser.objects.filter(email=email).exists() or \
#                 SignInUser.objects.filter(phone_number=phone_number).exists():
#             return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         # Hash the password before storing
#         hashed_password = make_password(password)

#         # Create the user
#         user = SignInUser.objects.create(
#             username=username,
#             email=email,
#             phone_number=phone_number,
#             password=hashed_password
#         )
#         print(user)
#         # Generate OTP
       
#         # You can also generate and send an authentication token here if needed

#         return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    


    


# class EmailverifyOTP(APIView):
#     def post(self, request):   
#         print(request.data)
#         # Extract email and OTP from request
#         email = request.data.get('Email')
#         print(email)

#         if SignInUser.objects.filter(email=email).exists():
                
#             return Response({'message': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        

#         otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
#         print(otp)
#         # Store OTP in the user object (assuming you have an 'otp' field in your user model)
#         request.session['OTP_check']=otp

#         # Send OTP to the user's email
#         subject = 'OTP Verification'
#         message = f'Your OTP for login is: {otp}'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email]
#         print(recipient_list)
#         # fail_silently=True
#         a=send_mail(subject, message, email_from, recipient_list, fail_silently=True,)
#         # print(a)
#         return Response({'message': 'OTP sent successfully and User created successfully', 'email': email,"otp":otp})

        
    

# # from django.contrib.auth.models import User
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class Send_userdetail(APIView):
#     def post(self, request):
#         print(request.data)
#         # Extract email from request data
#         email = request.data.get('Email')
#         print(email)
#         # Fetch user details based on the provided email
#         try:
#             user = SignInUser.objects.get(email=email)
#             print(user)
#         except SignInUser.DoesNotExist:
#             return Response({"error": "User not found for the provided email"}, status=404)

#         # Extract user details
#         user_details = {
#             "username": user.username,
#             "email": user.email,
#             "phone_number": user.phone_number,  # Assuming user has a 'phone_number' field
#             "password": user.password,  # Assuming you want to return the hashed password
#             # Add more user details as needed
#         }

#         # Return the user details in the response
#         return Response(user_details)


# class LoginAPIView(APIView):
#     def post(self, request):
#         # Extract email and password from request
#         email = request.data.get('Email')
#         password = request.data.get('password')

#         # Validate email format
#         print(email)
#         print(password)
       
#         # Retrieve user from database using email
#         try:
#             user = SignInUser.objects.get(email=email)
#         except SignInUser.DoesNotExist:
#             return Response({'message':'Email not found'},status=status.HTTP_404_NOT_FOUND)
#         if not check_password(password,user.password):
#             return Response({'message':'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)

#         serializer = SignInUserSerializer(user)

#         return Response({'message': 'Login successful', 'user': serializer.data})
        


# class ForgotPasswordAPIView(APIView):
#     def post(self, request):
#         # Extract email from request
#         email = request.data.get('Email')
        

#         # Validate email format
#         print("email is =",email)
        
#         try:
#             user = SignInUser.objects.get(email=email)
#         except SignInUser.DoesNotExist:
#             return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         # Generate OTP
#         otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
#         request.session['otp']=otp
#         otpp=request.session.get('otp')
#         print("session otp from forget ",otpp)
#         # Store OTP in the user object (assuming you have an 'otp' field in your user model)
        
#         # Send OTP to the user's email
#         subject = 'Forgot Password OTP'
#         message = f'Your OTP for password reset is: {otp}'
#         email_from = settings.EMAIL_HOST_USER
#         print("GGGGGGGGGGGGGGGGGGGGG",email_from)
#         recipient_list = [email]
#         print(recipient_list)
#         fail_silently=True
#         send_mail(subject, message, email_from, recipient_list, fail_silently,)
#         return Response({'message': 'OTP sent successfully', 'email': email,"otp":otp})

        
# class ResetPasswordAPIView(APIView):
#     def post(self, request):
#         # Extract email, OTP, new password, and confirm password from request      
#         email = request.data.get('Email')
#         # otp = request.data.get('otp')
        
#         new_password = request.data.get('new_password')
#         # confirm_password = request.data.get('confirm_password')

#         # Retrieve user from database using email
#         try:
#             user = SignInUser.objects.get(email=email)
#         except SignInUser.DoesNotExist:
#             return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
#         user.password=new_password
#         user.save()

#         return Response({'message': 'Password reset successful'})    


######################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import SignInUser

class SignInUserAPIView(APIView):
    def post(self, request):
        # Extract data from the request
        print(request.data)
        print("hi")
        username = request.data.get('username')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        request.session['username']=username
        # Check if the user already exists
        if SignInUser.objects.filter(email=email).exists() or \
                SignInUser.objects.filter(phone_number=phone_number).exists():
            return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before storing
        hashed_password = make_password(password)

        # Create the user
        user = SignInUser.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            password=hashed_password
        )
        print(user)
        # Generate OTP
       
        # You can also generate and send an authentication token here if needed

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    


class EmailverifyOTP(APIView):
    def post(self, request):   
        print(request.data)
        # Extract email and OTP from request
        email = request.data.get('Email')
        print(email)

        if SignInUser.objects.filter(email=email).exists():
                
            return Response({'message': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        

        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
        print(otp)
        # Store OTP in the user object (assuming you have an 'otp' field in your user model)
        request.session['OTP_check']=otp

        # Send OTP to the user's email
        subject = 'OTP Verification'
        message = f'Your OTP for login is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        print(recipient_list)
        # fail_silently=True
        a=send_mail(subject, message, email_from, recipient_list, fail_silently=True,)
        # print(a)
        return Response({'message': 'OTP sent successfully and User created successfully', 'email': email,"otp":otp})

        # otp_entered = request.data.get('otp') 

        # # Retrieve the stored OTP for the email (you may have to store this OTP somewhere in your application)
        # # stored_otp = '123456'  # This is a hardcoded OTP, replace it with your actual implementation
        
        # # Check if the entered OTP matches the stored OTP
        # if otp_entered == request.session['OTP']:
        #     # OTP verification successful
        #     return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        # else:
        #     # Incorrect OTP
        #     return Response({'message': 'Incorrect OTP'}, status=status.HTTP_400_BAD_REQUEST)
    

# from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

class Send_userdetail(APIView):
    def post(self, request):
        print(request.data)
        # Extract email from request data
        email = request.data.get('Email')
        print(email)
        # Fetch user details based on the provided email
        try:
            user = SignInUser.objects.get(email=email)
            print(user)
        except SignInUser.DoesNotExist:
            return Response({"error": "User not found for the provided email"}, status=404)

        # Extract user details
        user_details = {
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,  # Assuming user has a 'phone_number' field
            "password": user.password,  # Assuming you want to return the hashed password
            # Add more user details as needed
        }

        # Return the user details in the response
        return Response(user_details)


class LoginAPIView(APIView):
    def post(self, request):
        # Extract email and password from request
        email = request.data.get('Email')
        password = request.data.get('password')

        # Validate email format
        print(email)
        print(password)
        #try:
        #    validate_email(email)
        #except ValidationError:
         #   return Response({'message': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve user from database using email
        try:
            user = SignInUser.objects.get(email=email)

            

        except SignInUser.DoesNotExist:
            return Response({'message': 'Invalid email'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.password:
        	 return Response({'message':"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

        serializer = SignInUserSerializer(user)

        return Response({'message': 'Login successful', 'user': serializer.data})
        

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        # Extract email from request
        email = request.data.get('Email')
        

        # Validate email format
        print("email is =",email)
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     return Response({'message': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists with the provided email
        try:
            user = SignInUser.objects.get(email=email)
        except SignInUser.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
        request.session['otp']=otp
        otpp=request.session.get('otp')
        print("session otp from forget ",otpp)
        # Store OTP in the user object (assuming you have an 'otp' field in your user model)
        
        # Send OTP to the user's email
        subject = 'Forgot Password OTP'
        message = f'Your OTP for password reset is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        print("GGGGGGGGGGGGGGGGGGGGG",email_from)
        recipient_list = [email]
        print(recipient_list)
        fail_silently=True
        send_mail(subject, message, email_from, recipient_list, fail_silently,)
        return Response({'message': 'OTP sent successfully', 'email': email,"otp":otp})

        # a=send_mail("Forgot Password OTP ",
        #               f'Your OTP for password reset is: {otp}',
        #               "sangavichandhir@gmail.com",
        #               [email],
        #               fail_silently=True,)
        
        

    #     def send_mail(
    # subject: str,
    # message: str,
    # from_email: str | None,
    # recipient_list: list[str],
    # fail_silently: bool = ...,
    # auth_user: str | None = ...,
    # auth_password: str | None = ...,
    # connection: Any | None = ...,
class ResetPasswordAPIView(APIView):
    def post(self, request):
        # Extract email, OTP, new password, and confirm password from request      
        email = request.data.get('Email')
        # otp = request.data.get('otp')
        
        new_password = request.data.get('new_password')
        # confirm_password = request.data.get('confirm_password')

        # Retrieve user from database using email
        try:
            user = SignInUser.objects.get(email=email)
        except SignInUser.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check if OTP matches
        # OTP=request.session.get('otp')
        # print("session otp",OTP) 
        # if otp !=OTP  :
        #     return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if new password and confirm password match
        # if new_password != confirm_password:
        #     return Response({'message': 'New password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user's password
        user.password=new_password
        user.save()

        return Response({'message': 'Password reset successful'})            