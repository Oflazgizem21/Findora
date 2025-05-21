from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# CustomUser modelini admin paneline kaydet
admin.site.register(CustomUser, UserAdmin)