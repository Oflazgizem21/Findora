from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kanit, Bildirim

@receiver(post_save, sender=Kanit)
def kanit_status_change_notify(sender, instance, created, **kwargs):
    if not created and instance.status in ['approved', 'rejected']:
        # Kaybedene bildirim
        kaybeden_mesaj = (
            f"'{instance.secilen_esya.tanim}' eşyanız {instance.get_status_display()}! " +
            (f"Admin Mesajı: {instance.admin_mesaji}" if instance.admin_mesaji else "")
        )
        Bildirim.objects.create(
            kullanici=instance.kullanici,
            kanit=instance,
            mesaj=kaybeden_mesaj
        )

        if instance.status == 'approved':
            # Eşyaları güncelle
            if instance.ilgili_kayit:
                instance.ilgili_kayit.kayit_turu = 'bulundu'
                instance.ilgili_kayit.save()
            if instance.secilen_esya:
                instance.secilen_esya.kayit_turu = 'bulundu'
                instance.secilen_esya.save()
            
            # Bulan kişiye hak ekle (F() olmadan)
            bulan_kisi = instance.bulan_kisi
            if bulan_kisi:
                # Mevcut değeri alıp 1 artırıyoruz
                bulan_kisi.kaybettim_hakki += 1
                bulan_kisi.save()
                
                bulan_mesaj = (
                    f"'{instance.ilgili_kayit.tanim}' eşyasını sahibine ulaştırdığınız için " +
                    f"teşekkürler! 🎉 1 adet 'kaybettim' hakkı kazandınız 🌟 (Toplam hak: {bulan_kisi.kaybettim_hakki})"
                )
                Bildirim.objects.create(
                    kullanici=bulan_kisi,
                    kanit=instance,
                    mesaj=bulan_mesaj
                )