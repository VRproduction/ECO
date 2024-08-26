import requests
import json
import base64
import hashlib

class Payment():
    def __init__(self):
        self.base_url = f"https://epoint.az/api/1/"
        self.public_key = "i000200357"
        self.private_key = "1GtBKUDrM4FNBzQu43NZ5Oqq"
    
    def getHeaders(self):
        headers = {
            'Content-Type': 'application/json'
        }
        return headers  

    def get_data_and_signature(self, json_string):
        json_string = json.dumps(json_string)

        data = base64.b64encode(json_string.encode()).decode()

        sgn_string = self.private_key + data + self.private_key

        sha1_hash = hashlib.sha1(sgn_string.encode()).digest()

        signature = base64.b64encode(sha1_hash).decode()

        data = {
            "data": data,
            "signature": signature 
        }

        return data

    def checkout_request(self, amount, language):
        json_string = {
            "public_key": f'{self.public_key}',
            "amount": f"0.01",
            # "amount": f"{amount}",
            "currency": "AZN",
            "language": language,
            "description": "test payment",
            "order_id": "1"
        }
        response = requests.post(self.base_url+'request', json = self.get_data_and_signature(json_string), headers = self.getHeaders())
        response_data = response.json()
        return response_data

    def get_payment_status(self, transaction):
        json_string = {
            "public_key": f'{self.public_key}',
            "transaction": f"{transaction.value}",
        }
        response = requests.post(self.base_url+'get-status', json = self.get_data_and_signature(json_string), headers = self.getHeaders())
        response_data = response.json()
        return response_data
