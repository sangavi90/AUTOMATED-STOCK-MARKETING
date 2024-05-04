from .views import *

import pyotp
import http.client
import json
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Leg

class update_order(APIView):
        def update_leg_order_status(self):
            try:
                token = "AFH6577WNNSGC4TGXVLJWHVAQI"
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                logger.error("Invalid Token: The provided token is not valid.")
                raise e

            data = smartApi.generateSession(username, pwd, totp)
            jwt_token = data['data']['jwtToken']

            conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

            headers = {
                'X-PrivateKey': '4dPdQcGs',
                'Accept': 'application/json',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '192.168.0.102',
                'X-ClientPublicIP': '49.205.145.221',
                'X-MACAddress': '80-38-FB-B9-EE-20',
                'X-UserType': 'USER',
                'Authorization': jwt_token,
                'Content-Type': 'application/json'
            }

            # Fetch all legs from the database
            legs = Leg.objects.all()

            for leg in legs:

                if leg.uniqueorderid:  # Check if uniqueorderid is not None
                    try:
                        print(leg.uniqueorderid)
                        conn.request("GET", "/rest/secure/angelbroking/order/v1/details/" + leg.uniqueorderid, "", headers)
                        res = conn.getresponse()
                        data = res.read().decode("utf-8")
                        order_data = json.loads(data)

                        # Check if the response from Angel Broking is successful
                        print("kbkhdbf= ",order_data.get('status'))
                        if order_data.get('status') == True:
                            # Update the leg with the received order details
                            leg.orderstatus = order_data.get('data')['orderstatus']
                            leg.reason = order_data.get('data')["text"]
                            leg.save()
                        else:
                            print(f"Failed to fetch order details for uniqueorderid: {leg.uniqueorderid}")

                    except Exception as e:
                        print(f"Error occurred while fetching order details for uniqueorderid: {leg.uniqueorderid}")
                        print(e)
                        


            conn.close()

        # Schedule the update_leg_order_status function to run every 5 hours
        def get(self,request):
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.update_leg_order_status, 'interval', seconds=45)
            scheduler.start()

            return Response("Restarted storing orderstatus")

        # Call the schedule_update function to start scheduling the updates
        
