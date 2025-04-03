from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm , CustomLoginForm

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

#Giriş Yap Fonksiyorunu
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Giriş başarılı!')
                return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

#Çıkış Yap Fonksiyonu
def user_logout(request):
    logout(request)  # Kullanıcının oturumunu sonlandır
    messages.success(request, 'Başarıyla çıkış yapıldı.')
    return redirect('home')
