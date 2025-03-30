from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm 

#Ana Sayfaya Dönme Fonksiyonu
def home(request):
    return render(request, 'index.html', {'user': request.user})

#Kayıt Ol Fonksiyonu
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Kayıt işlemi başarılı!')  # Başarı mesajı
            return redirect('home')  # Ana sayfaya yönlendir
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

