import json
import requests
from django.http import JsonResponse
from django.conf import settings

def shipment_promises(request):
    url = f"https://daas-public-api.development.dev.woltapi.com/v1/venues/{settings.WOLT_VENUE_ID}/shipment-promises"

    # POST isteği için veri
    data = {
        "street": "19e Abbas Mirzə Şərifzadə, Baku 1008",
        "city": "Baku",
        "post_code": "örnek_posta_kodu",
        "lat": 40.36815635,  # Örnek koordinatlar
        "lon": 49.8210362,
        "language": "az",
        "min_preparation_time_minutes": 30,
        "scheduled_dropoff_time": "2024-03-05T14:15:22Z"
    }

    headers = {
        'Authorization': f'Bearer {settings.WOLT_API_KEY}',
        'Content-Type': 'application/json'
    }

    # POST isteği gönderme
    response = requests.post(url, json=data, headers=headers)

    # Yanıtı kontrol etme
    print(response.json())
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
