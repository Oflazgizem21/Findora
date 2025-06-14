from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('premium/', views.premium_sayfasi, name='premium_sayfasi'),
    path('kayip-esya-bildir/', views.kayip_esya_bildir, name='kayip_esya_bildir'),
    path('kaybettim/', lambda r: views.kayit_olustur(r, 'kaybettim'), name='kaybettim'),
    path('buldum/', lambda r: views.kayit_olustur(r, 'buldum'), name='buldum'),
    path('kayit/<int:pk>/duzenle/', views.kayit_duzenle, name='kayit_duzenle'),
    path('kayit/<int:pk>/sil/', views.kayit_sil, name='kayit_sil'),
    path('arama/', views.arama_sonuc, name='arama_sonuc'),
    path('yorum-yap/', views.yorum_yap, name='yorum_yap'),
    path('yorum_sil/<int:yorum_id>/', views.yorum_sil, name='yorum_sil'),
    path('esya/<int:id>/', views.esya_detay, name='esya_detay'),
    path('bildirim-detay/<int:bildirim_id>/', views.bildirim_detay, name='bildirim_detay'),
    path('bildirim-okundu/<int:bildirim_id>/', views.bildirim_okundu, name='bildirim_okundu'),
    path('iletisim/', views.iletisim, name='iletisim'),
]