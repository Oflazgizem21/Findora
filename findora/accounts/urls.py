from django.urls import path
from .views import home, register, user_login, user_logout, profilim, profil_guncelle

urlpatterns = [
    path('', home, name='home'),                    # Ana sayfa
    path('register/', register, name='register'),   # Kayıt olma sayfası
    path('login/', user_login, name='login'),       # Giriş yapma sayfası
    path('accounts/logout/', user_logout, name='logout'),
    path('profil/', profilim, name='profilim'),     # Profil sayfası
    path('profil/guncelle/', profil_guncelle, name='profil_guncelle'),  # Profil güncelleme sayfası
]