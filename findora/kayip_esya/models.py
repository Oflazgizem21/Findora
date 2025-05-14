from django.db import models
from django.conf import settings #kullanıcı modeli için gerekli

class Kayit(models.Model):
    TUR_SECIMLERI = [
        ('canta', 'Çanta'),
        ('telefon', 'Telefon'),
        ('cuzdan', 'Cüzdan'),
        ('diger', 'Diğer'),
    ]

    RENK_SECIMLERI = [
        ('siyah', 'Siyah'),
        ('beyaz', 'Beyaz'),
        ('mavi', 'Mavi'),
        ('kirmizi', 'Kırmızı'),
        ('diger', 'Diğer'),
    ]

    KAYIT_TURU_CHOICES = [
        ('kaybettim', 'Kaybettim'),
        ('buldum', 'Buldum'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 🧍 kullanıcı alanı
    tanim = models.CharField(max_length=255, verbose_name="Eşya Tanımı")
    tur = models.CharField(max_length=50, choices=TUR_SECIMLERI, verbose_name="Eşya Türü", default='Seçiniz')
    renk = models.CharField(max_length=50, choices=RENK_SECIMLERI, verbose_name="Eşya Rengi", default='Seçiniz')
    konum = models.CharField(max_length=255, verbose_name="Konum")
    resim = models.ImageField(upload_to='uploads/', verbose_name="Eşya Resmi", blank=True, null=True)
    tarih = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    kayit_turu = models.CharField(max_length=10, choices=KAYIT_TURU_CHOICES)  # buraya dikkat

    def __str__(self):
        return self.tanim
    
class Kanit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]
        
    ilgili_kayit = models.ForeignKey(Kayit, on_delete=models.CASCADE)  # Bu kaydın bulunduğu eşya
    aciklama = models.TextField()  # Kanıt açıklaması
    foto = models.ImageField(upload_to='kanitlar/', blank=True, null=True)  # Kanıt fotoğrafı
    kullanici = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kullanıcı")
    secilen_esya = models.ForeignKey(Kayit, on_delete=models.CASCADE, related_name='secilen_esya', null=True, blank=True)  # Kullanıcının seçtiği kayıp eşya
    tarih = models.DateTimeField(auto_now_add=True)  # Kanıt gönderim tarihi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_mesaji = models.TextField(blank=True, null=True, verbose_name="Admin Mesajı")

    def _str_(self):
        return f"Kanit - {self.kullanici.username if self.kullanici else 'Bilinmeyen'} - {self.ilgili_kayit.tanim}"