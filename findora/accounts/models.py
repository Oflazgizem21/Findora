from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):   # Yeni kullanıcı oluşturur.
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Email alanı zorunludur")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):     # Yönetici (admin) kullanıcı oluşturur.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):     # Kullanıcı modelini özelleştiriyoruz.
    email = models.EmailField(unique=True)  
    birthdate = models.DateField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']  

    objects = CustomUserManager()  #Özel UserManager ekledik

    def __str__(self):
        return self.email