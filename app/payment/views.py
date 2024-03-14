from django.shortcuts import render, redirect
from product.models import BasketItem
from .delivery.wolt import Delivery
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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
    if(context['items'].count() > 0):
        return render(request, 'delivery.html', context = context)
    else:
        return redirect("home")

def shipment_promises(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    street = request.GET.get('street')
    if lat and lon:
        delivery = Delivery(lat = lat, lon = lon, street = street)
        return delivery.shipment_promises()
    return JsonResponse({"message": "Please send lat and lon value"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deliveries(request):
    lat = request.data.get('lat')
    lon = request.data.get('lon')
    amount = request.data.get('amount')
    recipient_name = request.data.get('recipient_name')
    recipient_phone = request.data.get('recipient_phone')
    shipment_promise_id = request.data.get('shipment_promise_id')
    user_basket_items = BasketItem.objects.filter(user=request.user).order_by("pk")
    parcel_list = [item.to_dict_for_wolt_delivery() for item in user_basket_items]
    if lat and lon and amount and recipient_name and recipient_phone and parcel_list and shipment_promise_id:
        delivery = Delivery(lat = lat, lon = lon)
        return delivery.deliveries(amount = amount, recipient_name = recipient_name, recipient_phone = recipient_phone, parcel_list = parcel_list, shipment_promise_id = shipment_promise_id)
    return Response({"message": "Please enter correct datas."})