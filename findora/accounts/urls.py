from django.urls import path
from .views import register,user_login, home

urlpatterns = [
    path('', home, name='home'),                    # Ana sayfa
    path('register/', register, name='register'),   # Kayıt olma sayfası
    path('login/', user_login, name='login'),      # Giriş yapma sayfası  # Kayıt olma sayfası
]