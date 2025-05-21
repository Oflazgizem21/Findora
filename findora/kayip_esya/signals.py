from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kanit, Bildirim

@receiver(post_save, sender=Kanit)
def kanit_status_change_notify(sender, instance, created, **kwargs):
    if not created and instance.status in ['approved', 'rejected']:
        # 1️⃣ KAYBEDENE BİLDİRİM (ORJINAL)
        kaybeden_mesaj = (
            f"'{instance.secilen_esya.tanim}' eşyanız {instance.get_status_display()}! " +
            (f"Mesaj: {instance.admin_mesaji}" if instance.admin_mesaji else "")
        )
        Bildirim.objects.create(
            kullanici=instance.kullanici,
            kanit=instance,
            mesaj=kaybeden_mesaj
        )

        # 2️⃣ BULDURAN KİŞİYE BİLDİRİM (YENİ EKLENEN) ✅
        if instance.status == 'approved':  # Sadece onay durumunda
            # Eşyaları güncelle (SENİN EKLEDİĞİN KISIM)
            if instance.ilgili_kayit:
                instance.ilgili_kayit.kayit_turu = 'bulundu'
                instance.ilgili_kayit.save()
            if instance.secilen_esya:
                instance.secilen_esya.kayit_turu = 'bulundu'
                instance.secilen_esya.save()
            
            bulan_mesaj = (
                f"'{instance.ilgili_kayit.tanim}' eşyasını sahibine ulaştırdığınız için " +
                "teşekkürler! 🎉 İyilik puanınız +1 🌟"
            )
            Bildirim.objects.create(
                kullanici=instance.bulan_kisi,  # Bulduran kişi
                kanit=instance,
                mesaj=bulan_mesaj
            )