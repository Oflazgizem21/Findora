from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kanit, Bildirim

@receiver(post_save, sender=Kanit)
def kanit_status_change_notify(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'approved':
            mesaj = f"{instance.admin_mesaji or ''}"

            # Eşyaları güncelle
            if instance.ilgili_kayit:
                instance.ilgili_kayit.kayit_turu = 'bulundu'
                instance.ilgili_kayit.save()
            if instance.secilen_esya:
                instance.secilen_esya.kayit_turu = 'bulundu'
                instance.secilen_esya.save()

        elif instance.status == 'rejected':
            mesaj = f"{instance.admin_mesaji or ''}"
        else:
            return

        Bildirim.objects.create(
            kullanici=instance.kullanici,
            kanit=instance,
            mesaj=mesaj.strip()
        )
