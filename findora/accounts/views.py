from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm , CustomLoginForm, ProfilFotoForm
from kayip_esya.models import Kayit, GenelYorum, Bildirim, ContactMessage
from django.contrib.auth.decorators import login_required

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

@login_required
def profilim(request):
    kullanici = request.user

    # Kaybettim başvurularını say
    kaybettim_sayisi = Kayit.objects.filter(user=kullanici, kayit_turu='kaybettim').count()
    kalan_hak = max(3 - kaybettim_sayisi, 0)

    session_hak = request.session.get('kalan_kaybettim_hakki')
    if session_hak is not None:
        kalan_hak = session_hak
        del request.session['kalan_kaybettim_hakki']

    kaybettiklerim = Kayit.objects.filter(user=kullanici, kayit_turu='kaybettim')
    bulduklarim = Kayit.objects.filter(user=kullanici, kayit_turu='buldum')
    yorumlar = GenelYorum.objects.filter(user=kullanici).order_by('-tarih')  # Yorumları tarih sırasına göre sıralıyoruz
    bildirimler = Bildirim.objects.filter(kullanici=kullanici).order_by('-olusturulma_tarihi')
    kayip_bildirimler = Bildirim.objects.filter(kullanici=kullanici, kanit__isnull=False).order_by('-olusturulma_tarihi')
    iletisim_mesajlari = ContactMessage.objects.filter(user=kullanici).order_by('-created_at')

    if request.method == 'POST':
        form = ProfilFotoForm(request.POST, request.FILES, instance=kullanici)
        if form.is_valid():
            form.save()
            return redirect('profilim')
    else:
        form = ProfilFotoForm(instance=kullanici)

    return render(request, "profilim.html", {
        "kaybettiklerim": kaybettiklerim,
        "bulduklarim": bulduklarim,
        "user": kullanici,
        "form": form,
        "yorumlar": yorumlar,
        "bildirimler": bildirimler,  # Zil için
        "kayip_bildirimler": kayip_bildirimler,  # Sadece kayıp eşya bildirimleri için
        "kalan_kaybettim_hakki": kalan_hak,
        "iletisim_mesajlari": iletisim_mesajlari,
    })

@login_required
def profil_guncelle(request):
    if request.method == 'POST':
        user = request.user

        user.full_name = request.POST.get('full_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        birthdate = request.POST.get('birthdate')
        user.birthdate = birthdate if birthdate else None

        if 'profile_pic' in request.FILES:
            user.profile_photo = request.FILES['profile_pic']

        user.save()
        return redirect('profilim')

    return redirect('profilim')