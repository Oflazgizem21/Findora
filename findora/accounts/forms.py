from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

#Kullanıcı Kayıt Formu
class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tam Adınız'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'})
    )
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Doğum Tarihi', 'type': 'date'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'birthdate', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form alanlarına Bootstrap sınıfları
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Kullanıcı Adı'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Şifre'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Şifre Tekrar'})

