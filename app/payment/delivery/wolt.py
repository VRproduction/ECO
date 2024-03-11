import json
import requests
from django.http import JsonResponse
from django.conf import settings

class Delivery():
    def __init__(self):
        self.url = f"https://daas-public-api.development.dev.woltapi.com/v1/venues/{settings.WOLT_VENUE_ID}/shipment-promises"

        # self   
    def shipment_promises(self):
        data = {
            "street": "19e Abbas Mirzə Şərifzadə, Baku 1008",
            "city": "Baku",
            "lat": 40.36815635, 
            "lon": 49.8210362,
            "language": "az",
        }

        headers = {
            'Authorization': f'Bearer {settings.WOLT_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(self.url, json=data, headers=headers)

        if response.status_code == 201:
            # JSON yanıtını Python sözlük veri yapısına dönüştürme
            response_data = response.json()

            # Örneğin, gönderi detaylarına erişmek için
            pickup_location = response_data["pickup"]["location"]["formatted_address"]
            dropoff_location = response_data["dropoff"]["location"]["formatted_address"]
            price = response_data["price"]["amount"]

            # JSON yanıtını işleyerek uygun bir HTTP yanıtı oluşturma
            return JsonResponse({
                "pickup_location": pickup_location,
                "dropoff_location": dropoff_location,
                "price": price
            })
        else:
            return JsonResponse({"message": "İstek gönderilirken bir hata oluştu", "status_code": response.status_code})
