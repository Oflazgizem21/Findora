from django.urls import path
from .views import register, home

urlpatterns = [
    path('', home, name='home'),                    # Ana sayfa
    path('register/', register, name='register'),   # Kayıt olma sayfası
]