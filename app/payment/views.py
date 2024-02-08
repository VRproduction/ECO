from django.shortcuts import render

def payment(request):
    return render(request, 'payment.html')

def success(request):
    return render(request, 'success.html')

def failed(request):
    return render(request, 'failed.html')

def result(request):
    return render(request, 'result.html')