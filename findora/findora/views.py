from django.shortcuts import render

def hakkimizda(request):
    return render(request, 'hakkimizda.html')

def iletisim(request):
    return render(request, 'iletisim.html')
