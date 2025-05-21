from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#Kullanıcı Kayıt Formu
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={
            'required': 'Lütfen tam adınızı girin.',
            'max_length': 'Ad çok uzun, en fazla 255 karakter olabilir.',
        },
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tam Adınız'})
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Lütfen e-posta adresinizi girin.',
            'invalid': 'Geçerli bir e-posta adresi girin.',
        },
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'})
    )
    birthdate = forms.DateField(
        required=True,
        error_messages={
            'required': 'Lütfen doğum tarihinizi girin.',
            'invalid': 'Geçerli bir tarih formatı girin. (GG/AA/YYYY)',
        },
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Doğum Tarihi', 'type': 'date'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'birthdate', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Şifre en az 8 karakter olmalıdır.")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Şifreler eşleşmiyor.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        allowed_domains = ['gmail.com', 'hotmail.com', 'outlook.com']
        domain = email.split('@')[-1] if '@' in email else ''
        
        if not domain in allowed_domains:
            raise ValidationError("Sadece gmail.com, hotmail.com veya outlook.com uzantılı e-posta adresleri kabul edilir.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Kullanıcı Adı'})
        self.fields['username'].error_messages = {
            'required': 'Kullanıcı adı zorunludur.',
            'invalid': 'Geçerli bir kullanıcı adı girin.',
            'unique': 'Bu kullanıcı adı zaten kullanılıyor.',
        }

        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Şifre'})
        self.fields['password1'].error_messages = {
            'required': 'Lütfen bir şifre belirleyin.'
        }

        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Şifre Tekrar'})
        self.fields['password2'].error_messages = {
            'required': 'Lütfen şifrenizi tekrar girin.'
        }

#Giriş Yapma Formu
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-Posta'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'})
    )        

class ProfilFotoForm(forms.ModelForm):  # Profil fotoğrafı yükleme formu
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'birthdate', 'profile_photo']

class ProfilGuncellemeForm(forms.ModelForm):    # Profil güncelleme formu*
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'birthdate', 'profile_photo']