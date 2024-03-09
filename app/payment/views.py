from django.shortcuts import render
from product.models import BasketItem

def payment(request):
    return render(request, 'payment.html')

def success(request):
    return render(request, 'success.html')

def failed(request):
    return render(request, 'failed.html')

def result(request):
    return render(request, 'result.html')

def map(request):
    context = {
        "items": BasketItem.objects.filter(user = request.user).order_by("pk")
    }
    return render(request, 'delivery.html', context = context)
