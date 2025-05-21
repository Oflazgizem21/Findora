from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, timedelta
from .forms import KayitForm, YorumForm, ContactForm
from .models import Kayit, GenelYorum, Kanit, Bildirim
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

def index(request):
    # Yorumları veritabanından alıyoruz
    yorumlar = GenelYorum.objects.all().order_by('-tarih')   # Yorumları tarihe göre sıralıyoruz ve GenelYorum modelini kullanıyoruz
    return render(request, 'index.html', {'yorumlar': yorumlar})

def premium_sayfasi(request):   # Premium sayfasına yönlendirme
    return render(request, 'premium.html')

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
                    messages.error(request, "Ücretsiz kullanıcılar en fazla 3 'Kaybettim' ilanı ekleyebilir.")
                    return redirect('premium_sayfasi')
                
                #kalan hakkı hesapla
                request.session['kalan_kaybettim_hakki'] = max(3 - (kaybettim_sayisi+1), 0)

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
        post_data = request.POST.copy()

        #Eğer "Diğer" seçeneği seçilmişse ve kullanıcı kutuya bir şey yazmışsa onu asıl alana ata
        if post_data.get("tur") == "Diğer" and post_data.get("diger_tur"):
            post_data["tur"] = post_data.get("diger_tur")

        if post_data.get("renk") == "Diğer" and post_data.get("diger_renk"):
            post_data["renk"] = post_data.get("diger_renk")


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

#arama fonksiyonu
@login_required
def arama_sonuc(request):
    query = request.GET.get('q', '')
    renk = request.GET.get('renk', '')
    konum = request.GET.get('konum', '')
    durum = request.GET.get('durum', 'buldum')  # Varsayılan 'buldum'

    # 'kaybettim' durumundaki kayıtları ASLA gösterme
    kayitlar = Kayit.objects.exclude(kayit_turu='kaybettim')

    # Anahtar kelime varsa SADECE 'buldum' kayıtlarını filtrele
    if query:
        kayitlar = kayitlar.filter(
            Q(kayit_turu='buldum') & (
                Q(tanim__icontains=query) |
                Q(tur__icontains=query) |
                Q(renk__icontains=query) |
                Q(konum__icontains=query)
            )
        )
    # Anahtar kelime yoksa durum filtresini uygula
    elif durum in ['buldum', 'bulundu']:
        kayitlar = kayitlar.filter(kayit_turu=durum)

    # Kullanıcının kendi eklediği 'buldum' kayıtlarını gösterme
    kayitlar = kayitlar.exclude(user=request.user, kayit_turu='buldum')

    # Diğer filtreler
    if renk:
        kayitlar = kayitlar.filter(renk__icontains=renk)
    if konum:
        kayitlar = kayitlar.filter(konum__icontains=konum)
    
    # Burada queryset'i listeye çeviriyoruz
    kayitlar = list(kayitlar)
      # Yeni kayıtları belirle
    for kayit in kayitlar:
        kayit.yeni_mi = (datetime.now().date() - kayit.tarih.date()) <= timedelta(days=3)
        
    # Yeni olanlar en üstte, sonra tarih azalan şekilde sırala
    kayitlar = sorted(kayitlar, key=lambda x: (not x.yeni_mi, -x.tarih.timestamp()))
    return render(request, 'arama_sonuc.html', {
        'kayitlar': kayitlar,
        'query': query,
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

@login_required
def yorum_sil(request, yorum_id):
    yorum = get_object_or_404(GenelYorum, id=yorum_id, user=request.user)
    if request.method == "POST":
        yorum.delete()
        return redirect('profilim')
    return redirect('profilim')

def profilim(request):
    bildirimler = Bildirim.objects.filter(kullanici=request.user).order_by('-olusturulma_tarihi')
    
    context = {
        'bildirimler': bildirimler,
        # varsa diğer context verilerini de ekle
    }
    return render(request, 'profilim.html', context)

def bildirim_detay(request, bildirim_id):
    bildirim = get_object_or_404(Bildirim, id=bildirim_id, kullanici=request.user)
    okunmamis_bildirim_sayisi = Bildirim.objects.filter(kullanici=request.user, okundu=False).count()
    context = {
        'bildirim': bildirim,
        'kanit': bildirim.kanit,
        'okunmamis_bildirim_sayisi': okunmamis_bildirim_sayisi,
    }
    html = render_to_string('bildirim_detay_modal.html', context, request=request)
    return HttpResponse(html)

def bildirim_okundu(request, bildirim_id):
    if request.method == "POST" and request.user.is_authenticated:
        bildirim = get_object_or_404(Bildirim, id=bildirim_id, kullanici=request.user)
        if not bildirim.okundu:
            bildirim.okundu = True
            bildirim.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
    
def iletisim(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False) 
            if request.user.is_authenticated: #Oturum açıksa kullanıcıyı bağla
                contact.user = request.user
            contact.save() #şimdi kaydet
            messages.success(request, 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.')
            return redirect('iletisim')
    else:
        form = ContactForm()
    
    return render(request, 'iletisim.html', {'form': form})