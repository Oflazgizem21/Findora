from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

#Kendi kullanıcı oluşturma metodlarımız tanımlanır
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email alanı zorunludur")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
#Django'nun hazır kayıt oluşturma metodu override edilir
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  
    birthdate = models.DateField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']  

    objects = CustomUserManager()  #Özel UserManager ekledik
    class Meta:
        swappable = 'AUTH_USER_MODEL'