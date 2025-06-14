# Generated by Django 5.2.1 on 2025-05-19 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayip_esya', '0007_genelyorum_kanit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bildirim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesaj', models.CharField(max_length=255)),
                ('olusturulma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('okundu', models.BooleanField(default=False)),
                ('kanit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kayip_esya.kanit')),
                ('kullanici', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ad Soyad')),
                ('email', models.EmailField(max_length=254, verbose_name='E-posta')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefon')),
                ('subject', models.CharField(choices=[('general', 'Genel Soru'), ('lost-item', 'Kayıp Eşya'), ('found-item', 'Bulunan Eşya'), ('feedback', 'Geri Bildirim'), ('business', 'İş Birliği'), ('other', 'Diğer')], max_length=20, verbose_name='Konu')),
                ('message', models.TextField(verbose_name='Mesaj')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('admin_cevabi', models.TextField(blank=True, null=True, verbose_name='Admin Cevabı')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'İletişim Mesajı',
                'verbose_name_plural': 'İletişim Mesajları',
                'ordering': ['-created_at'],
            },
        ),
    ]
