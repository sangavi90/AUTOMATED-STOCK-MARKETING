from .imports import *
class GetTradeBookAPIView(APIView):
    def get(self, request):
        try:
            # Token for generating TOTP
            token = "AFH6577WNNSGC4TGXVLJWHVAQI"
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            return Response({'error': 'Failed to generate TOTP token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Replace these values with your actual credentials
        username = 'S2098754'
        pwd = '2024'

        # Initialize SmartConnect with your API key
        smartApi = SmartConnect('4dPdQcGs')

        try:
            # Generate session using username, password, and TOTP
            data = smartApi.generateSession(username, pwd, totp)

            # Check if session generation was successful
            if not data['status']:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract JWT token from the session data
            jwt_token = data['data']['jwtToken']
        except Exception as e:
            return Response({'error': 'Failed to generate session.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Establish a connection to the trading platform API
            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
            
            payload=''
            # Define headers for the request
            headers = {
                'Authorization':jwt_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP':'192.168.0.101' ,
                'X-ClientPublicIP': '49.205.145.221',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-PrivateKey': '4dPdQcGs'
            }

            # Make a GET request to retrieve the trade book
            conn.request("GET", "/rest/secure/angelbroking/order/v1/getTradeBook", headers=headers)

            # Get the response from the server
            res = conn.getresponse()

            # Read and decode the response data
            data = res.read().decode("utf-8")

            # Close the connection
            conn.close()

            # Return the response data along with the status code
            return Response(json.loads(data), status=res.status)

        except Exception as e:
            # Return an error response if any exception occurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)