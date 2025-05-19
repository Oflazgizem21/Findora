from django.contrib import admin
from .models import ContactMessage, Bildirim
from django.contrib.auth import get_user_model
from django.utils.html import format_html

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

