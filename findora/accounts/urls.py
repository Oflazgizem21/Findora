from django.urls import path
from .views import home, register, user_login, user_logout, profilim

urlpatterns = [
    path('', home, name='home'),                    # Ana sayfa
    path('register/', register, name='register'),   # Kayıt olma sayfası
    path('login/', user_login, name='login'),       # Giriş yapma sayfası
    path('logout/', user_logout, name='logout'),    # Çıkış yapma sayfası
    path('profil/', profilim, name='profilim'),     # Profil sayfası
]