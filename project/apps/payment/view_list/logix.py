from django.http import JsonResponse
from ..logistic.logix import Logix  # Logix sınıfını içe aktarın

def test_logix_order(request):
    # Test verileri
    orders = [
        {"Product": 1, "Quantity": 2, "Price": 8.60},
        {"Product": 2, "Quantity": 2, "Price": 7.51},
    ]

    # Logix sınıfını kullan
    logix = Logix()
    response = logix.send_post_order(orders)

    # # API yanıtını döndür
    return JsonResponse(response)