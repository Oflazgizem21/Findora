import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayip_esya', '0006_alter_kayit_konum_alter_kayit_renk_alter_kayit_tanim_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GenelYorum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yorum', models.TextField(max_length=500, verbose_name='Yorum')),
                ('tarih', models.DateTimeField(auto_now_add=True, verbose_name='Yorum Tarihi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kanit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aciklama', models.TextField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='kanitlar/')),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Beklemede'), ('approved', 'Onaylandı'), ('rejected', 'Reddedildi')], default='pending', max_length=20)),
                ('admin_mesaji', models.TextField(blank=True, null=True, verbose_name='Admin Mesajı')),
                ('ilgili_kayit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kayip_esya.kayit')),
                ('kullanici', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
                ('secilen_esya', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secilen_esya', to='kayip_esya.kayit')),
            ],
        ),
    ]
