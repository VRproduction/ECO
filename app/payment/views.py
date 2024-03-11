from django.shortcuts import render
from product.models import BasketItem
from .delivery.wolt import Delivery

def payment(request):
    return render(request, 'payment.html')

def success(request):
    return render(request, 'success.html')

def failed(request):
    return render(request, 'failed.html')

def result(request):
    return render(request, 'result.html')

def map(request):
    delivery = Delivery()
    delivery.shipment_promises()
    print("salam")
    context = {
        "items": BasketItem.objects.filter(user = request.user).order_by("pk")
    }
    return render(request, 'delivery.html', context = context)
