from django.shortcuts import render

def dashboard_principal(request):
    return render(request, 'index.html')