from django import forms
from .models import Kayit, Kanit, GenelYorum, ContactMessage

class KayitForm(forms.ModelForm):
    custom_tur = forms.CharField(required=False, widget=forms.HiddenInput())
    custom_renk = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Kayit
        fields = ['tanim', 'tur', 'renk', 'konum', 'resim']

        widgets = {
            'tanim': forms.TextInput(attrs={
                'placeholder': 'Örnek: Fermuarı bozuk siyah çanta',
                'class': 'form-input'
            }),
            'konum': forms.TextInput(attrs={
                'placeholder': 'Örnek: Trabzon Meydan Parkı',
                'class': 'form-input'
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.tur == 'diger':
            instance.tur = self.cleaned_data.get('custom_tur', 'Belirtilmedi')
        if instance.renk == 'diger':
            instance.renk = self.cleaned_data.get('custom_renk', 'Belirtilmedi')
        if commit:
            instance.save()
        return instance
    
class KanitForm(forms.ModelForm):
    class Meta:
        model = Kanit
        fields = ['aciklama', 'foto']  # isim ve soyisim çıkarıldı

class YorumForm(forms.ModelForm):
    class Meta:
        model = GenelYorum
        fields = ['yorum']  # Yalnızca 'yorum' alanını alıyoruz

    yorum = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Yorumunuzu buraya yazın...', 'rows': 5, 'cols': 40}), label='Yorum')

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız ve soyadınız',
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresiniz',
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefon numaranız (isteğe bağlı)',
                'id': 'phone'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'id': 'subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mesajınızı detaylı şekilde yazın...',
                'rows': 5,
                'id': 'message'
            }),
        }