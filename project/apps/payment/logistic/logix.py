import requests
import json
import base64
import hashlib

class Logix():
    def __init__(self):
        self.base_url = f"http://azews02.logixvps.cloud:3457/logix/pos/qupiec/db/post/request"
        self.autharization = "MTcyMzgxNTE5MTEyMzE3MjM4MTUxOTExMjMxNzIzODE1MTkxMTIz"
    
    def getHeaders(self):
        headers = {
            'Authorization': f'{self.autharization}',
            'Content-Type': 'application/json'
        }
        return headers  

    def send_post_order(self, orders):
        # orders = [
        #     {"Product": 1, "Quantity": 2, "Price": 8.60},
        #     {"Product": 2, "Quantity": 2, "Price": 7.51},
        # ]
        data = {
            "Method": "POST_ORDER",
            "Orders": orders
        }
        
        try:
            # POST isteğini gönder
            response = requests.post(self.base_url, json=data, headers=self.getHeaders())
            
            # Yanıt durumunu kontrol et
            if response.status_code == 200:
                return response.json()  # Başarılı yanıt
            else:
                return {"error": f"HTTP {response.status_code}", "message": response.text}
        except requests.exceptions.RequestException as e:
            return {"error": "RequestException", "message": str(e)}
