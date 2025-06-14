from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kayip_esya', '0005_kayit_kayit_turu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kayit',
            name='konum',
            field=models.CharField(max_length=255, verbose_name='Konum'),
        ),
        migrations.AlterField(
            model_name='kayit',
            name='renk',
            field=models.CharField(choices=[('siyah', 'Siyah'), ('beyaz', 'Beyaz'), ('mavi', 'Mavi'), ('kirmizi', 'Kırmızı'), ('diger', 'Diğer')], default='Seçiniz', max_length=50, verbose_name='Eşya Rengi'),
        ),
        migrations.AlterField(
            model_name='kayit',
            name='tanim',
            field=models.CharField(max_length=255, verbose_name='Eşya Tanımı'),
        ),
        migrations.AlterField(
            model_name='kayit',
            name='tur',
            field=models.CharField(choices=[('canta', 'Çanta'), ('telefon', 'Telefon'), ('cuzdan', 'Cüzdan'), ('diger', 'Diğer')], default='Seçiniz', max_length=50, verbose_name='Eşya Türü'),
        ),
    ]
