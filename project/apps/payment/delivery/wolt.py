import json
import requests
from django.http import JsonResponse
from django.conf import settings
from ..models import Wolt

class Delivery():
    def __init__(self, lat, lon, street = None):
        self.base_url = f"https://daas-public-api.wolt.com/v1/venues/{settings.WOLT_VENUE_ID}/"
        self.test_url = f"https://daas-public-api.development.dev.woltapi.com/v1/venues/{settings.WOLT_VENUE_ID_TEST}/"
        self.lat = lat
        self.lon = lon
        self.street = street

    def getHeaders(self):
        headers = {
            'Authorization': f'Bearer {settings.WOLT_API_KEY_TEST}',
            'Content-Type': 'application/json'
        }
        return headers
    
    def shipment_promises(self):
        data = {
            "street": self.street,
            "city": "Baku",
            "lat": self.lat, 
            "lon": self.lon,
            "language": "az",
            "min_preparation_time_minutes": 20,
        }

        response = requests.post(self.test_url+'shipment-promises', json = data, headers = self.getHeaders())
        response_data = response.json()
        
        return response_data
    
    def deliveries(self, amount, recipient_name, recipient_phone, dropoff_comment, parcel_list, shipment_promise_id):
        customer_support = Wolt.objects.first()
        data = {
            "pickup": {
                "options": {
                    "min_preparation_time_minutes": 20
                }
            },
            "dropoff": {
                "location": {
                    "coordinates": {
                        "lat": self.lat,
                        "lon": self.lon
                    }
                },
                "comment": dropoff_comment,
            },
            "price": {
                "amount": float(amount)*100,
                "currency": "AZN"
            },
            "recipient": {
                "name": recipient_name,
                "phone_number": recipient_phone,
            },
            "parcels":  parcel_list,
            "shipment_promise_id": shipment_promise_id,
            "customer_support": {
               
            },
        }
        if(customer_support):
            if customer_support.customer_url:
                data["customer_support"]["url"] = customer_support.customer_url
            if customer_support.customer_email:
                data["customer_support"]["email"] = customer_support.customer_email
            if customer_support.customer_phone_number:
                data["customer_support"]["phone_number"] = customer_support.customer_phone_number

        response = requests.post(self.test_url+'deliveries', json = data, headers = self.getHeaders())
        response_data = response.json()
        print(response)
        return response_data


