from rest_framework.views import APIView
from rest_framework.response import Response
from .models import company_name
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import company_name
import requests
from rest_framework import status

class MarketpriceAPIView(APIView):
    def get(self, request):
        # Fetch data from the API
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Iterate through the data and store tokens for matching companies with exch_seg 'NSE' and tradingsymbol ending with '-EQ'
            for item in data:
                if item['exch_seg'] == 'NSE' and item['symbol'].endswith('-EQ'):
                    company = company_name.objects.filter(company_name=item['name']).first()
                    if company:
                        company.symboltoken = item['token']
                        company.save()

            return Response({'message': 'Tokens saved successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to fetch data from the API'}, status=response.status_code)