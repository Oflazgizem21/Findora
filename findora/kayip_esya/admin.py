from django.contrib import admin
from .models import Kayit, Kanit, ContactMessage, Bildirim
from .forms import KayitForm, KanitForm
from django.contrib.auth import get_user_model
from django.utils.html import format_html

@admin.register(Kanit)
class KanitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'kullanici_email', 'ilgili_kayit_tanim', 'ilgili_kayit_tur', 
        'ilgili_kayit_renk', 'ilgili_kayit_konum', 'ilgili_kayit_resim', 
        'secilen_esya_tanim', 'secilen_esya_tur', 'secilen_esya_renk',
        'secilen_esya_konum', 'secilen_esya_resim', 'tarih'
    )
    list_filter = ('status', 'tarih')
    search_fields = ('ilgili_kayit__tanim',)
    readonly_fields = ('kullanici_email',)
    exclude = ('aciklama',)
    actions = ['onayla', 'reddet']

    def kullanici_email(self, obj):
        return obj.kullanici.email if obj.kullanici else "Belirtilmemiş"
    def ilgili_kayit_tanim(self, obj):
        return obj.ilgili_kayit.tanim
    def secilen_esya_tanim(self, obj):
        return obj.secilen_esya.tanim
    def ilgili_kayit_tur(self, obj):
        return obj.ilgili_kayit.tur
    def secilen_esya_tur(self, obj):
        return obj.secilen_esya.tur
    def ilgili_kayit_renk(self, obj):
        return obj.ilgili_kayit.renk
    def secilen_esya_renk(self, obj):
        return obj.secilen_esya.renk
    def ilgili_kayit_konum(self, obj):
        return obj.ilgili_kayit.konum
    def secilen_esya_konum(self, obj):
        return obj.secilen_esya.konum
    def ilgili_kayit_resim(self, obj):
        if obj.ilgili_kayit.resim:
            return format_html('<img src="{}" width="50" />', obj.ilgili_kayit.resim.url)
        return "Resim Yok"
    def secilen_esya_resim(self, obj):
        if obj.secilen_esya.resim:
            return format_html('<img src="{}" width="50" />', obj.secilen_esya.resim.url)
        return "Resim Yok"

    def onayla(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Seçilen kanıtlar onaylandı.")

    def reddet(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Seçilen kanıtlar reddedildi.")

@admin.register(Kayit)
class KayitAdmin(admin.ModelAdmin):
    form = KayitForm
    list_display = ('tanim', 'tur', 'renk', 'kayit_turu', 'tarih')
    search_fields = ('tanim', 'konum')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'get_subject_display', 'created_at', 'kisa_cevap')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


    fields = ('user', 'name', 'email', 'phone', 'subject', 'message', 'created_at', 'admin_cevabi')  # 💬 Admin cevabı ve user ekledik
    
    def get_subject_display(self, obj):
        return obj.get_subject_display()
    get_subject_display.short_description = 'Konu'

    def kisa_mesaj(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    kisa_mesaj.short_description = "Mesaj"

    def kisa_cevap(self, obj):
        return obj.admin_cevabi[:50] + "..." if obj.admin_cevabi else "Henüz yok"
    kisa_cevap.short_description = "Admin Cevabı"

    def save_model(self, request, obj, form, change):
        if change and 'admin_cevabi' in form.changed_data:
            if obj.admin_cevabi:  # Cevap boş değilse
                obj.save()  # Değişiklikleri kaydet
                if obj.user:  # Kullanıcı kayıtlıysa
                    Bildirim.objects.create(
                        kullanici=obj.user,
                        mesaj=f"İletişim formunuza admin tarafından cevap verildi: {obj.admin_cevabi[:50]}..."
                    )
        super().save_model(request, obj, form, change)

