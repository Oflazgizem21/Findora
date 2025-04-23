from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kayip-esya-bildir/', views.kayip_esya_bildir, name='kayip_esya_bildir'),
    path('buldum/', views.buldum, name='buldum'),
    path('kaybettim/', views.kaybettim, name='kaybettim'),
]