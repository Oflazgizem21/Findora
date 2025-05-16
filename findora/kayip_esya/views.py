from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from .forms import KayitForm, YorumForm
from .models import Kayit, GenelYorum, Kanit
from django.contrib import messages

def index(request):
    # Yorumları veritabanından alıyoruz
    yorumlar = GenelYorum.objects.all().order_by('-tarih')   # Yorumları tarihe göre sıralıyoruz ve GenelYorum modelini kullanıyoruz
    return render(request, 'index.html', {'yorumlar': yorumlar})


@login_required
def kayip_esya_bildir(request):
    return render(request, 'kayip_esya_bildir.html')

@login_required
def kayit_olustur(request, tur):
    if request.method == 'POST':
        form = KayitForm(request.POST, request.FILES)
        if form.is_valid():
            kayit = form.save(commit=False)
            kayit.user = request.user
            kayit.kayit_turu = tur

            # 🔒 Kayıp eşyalar için en fazla 3 kayıt sınırı
            if tur == 'kaybettim':
                kaybettim_sayisi = Kayit.objects.filter(user=request.user, kayit_turu='kaybettim').count()
                if kaybettim_sayisi >= 3:
                    return redirect('premium_sayfasi')

            # "Diğer" seçeneği için özelleştirme
            if request.POST.get('tur') == 'diger':
                kayit.tur = request.POST.get('custom_tur', 'Belirtilmedi')
            if request.POST.get('renk') == 'diger':
                kayit.renk = request.POST.get('custom_renk', 'Belirtilmedi')

            kayit.save()
            return redirect('home')
    else:
        form = KayitForm()
    return render(request, f'{tur}.html', {'form': form})

@login_required
def kayit_duzenle(request, pk):
    kayit = get_object_or_404(Kayit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = KayitForm(request.POST, request.FILES, instance=kayit)
        if form.is_valid():
            form.save()
            return redirect('profilim')
    else:
        form = KayitForm(instance=kayit)
    return render(request, 'kayit_duzenle.html', {'form': form})

@login_required
def kayit_sil(request, pk):
    kayit = get_object_or_404(Kayit, pk=pk, user=request.user)
    kayit.delete()
    return redirect('profilim')

@login_required
def arama_sonuc(request):
    query = request.GET.get('q', '')
    renk = request.GET.get('renk', '')
    konum = request.GET.get('konum', '')
    durum = request.GET.get('durum', 'buldum')

    kayitlar = Kayit.objects.all()

    if durum in ['buldum', 'bulundu']:
        kayitlar = kayitlar.filter(kayit_turu=durum)

    if query:
        kayitlar = kayitlar.filter(
            Q(tanim__icontains=query) |
            Q(tur__icontains=query) |
            Q(renk__icontains=query) |
            Q(konum__icontains=query)
        )

    if renk:
        kayitlar = kayitlar.filter(renk__icontains=renk)
    if konum:
        kayitlar = kayitlar.filter(konum__icontains=konum)

    return render(request, 'arama_sonuc.html', {
        'query': query,
        'kayitlar': kayitlar,
    })

@login_required
def esya_detay(request, id):
    kayit = get_object_or_404(Kayit, id=id, kayit_turu='buldum')

    kayip_kayitlari = Kayit.objects.filter(user=request.user, kayit_turu='kaybettim')
    if not kayip_kayitlari.exists():
        messages.warning(request, "Bu eşyaya talip olmak için önce bir kayıp bildirimi yapmalısınız.")
        return redirect('kaybettim')

    if request.method == 'POST':
        secilen_esya_id = request.POST.get('secilen_esya')
        secilen_esya = get_object_or_404(Kayit, id=secilen_esya_id)

        # 🔧 BURASI: kullanıcıyı ekliyoruz!
        kanit = Kanit(
            ilgili_kayit=kayit,
            secilen_esya=secilen_esya,
            kullanici=request.user  # ✅ GEREKLİ OLAN KISIM BU
        )
        kanit.save()

        messages.success(request, "Kanıt gönderildi. En kısa sürede değerlendirilecektir.")
        return redirect('profilim')

    return render(request, 'esya_detay.html', {
        'kayit': kayit,
        'kayip_kayitlari': kayip_kayitlari
    })

@login_required
def yorum_yap(request):
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yeni_yorum = form.save(commit=False)
            yeni_yorum.user = request.user  # Yorumun sahibi olarak kullanıcıyı ekliyoruz
            yeni_yorum.save()
            return redirect('index')  # Yorum başarıyla eklendikten sonra index'e yönlendir
    else:
        form = YorumForm()

    return render(request, 'yorum_yap.html', {'form': form})
