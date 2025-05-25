# 🧭 FINDORA - Kayıp Eşya Takip Sistemi

Findora, insanların kaybettikleri ya da buldukları eşyaları kolayca paylaşabildiği ve eşya sahiplerinin eşyalarını tekrar bulmasına yardımcı olmayı amaçlayan bir web uygulamasıdır.

## 🚀 Proje Hakkında

**Findora**, insanların kaybettikleri veya buldukları eşyaları dijital bir platform üzerinden kolayca paylaşmalarını ve kayıp eşyaların sahiplerine güvenli bir şekilde ulaşmasını amaçlayan bir web uygulamasıdır. Bu proje, **Software Engineering** dersi kapsamında 3 kişilik bir ekip tarafından geliştirilmiştir.

Kullanıcılar sistem üzerinde:
- 🔎 Kayıp ya da bulunan eşya ilanı oluşturma
  - Eşya tanımı, türü, rengi, konumu gibi bilgileri girerek detaylı ilan oluşturulabilir.
  - İsteğe bağlı olarak eşya fotoğrafı da yüklenebilir.
- 🎯 Eşya filtreleme özelliği
  - Eşya türü, rengi ve konum gibi kriterlere göre hızlıca filtreleme yapılabilir.
- 🔗 Eşya eşleştirme talebi
  - Bir eşyayı kendi kaybettiği eşya olduğunu düşünen kullanıcı, sistem üzerinden eşleştirme talebi gönderir.
- 📝 Yorum sistemi ile etkileşim
  - Kullanıcılar ilanlara yorum yaparak bilgi ekleyebilir veya sorularını iletebilir.


## 👥 Takım Üyeleri

| İsim    | Rol              |
|---------|------------------|
| Gizem Oflaz  | Takım Kaptanı, Full-Stack Geliştirici    |
| Zeynep Türkan Aytaç | Kod Kontrolcüsü, Back-end Geliştirici  |
| Özlem Özdemirci  | Takım Üyesi, Front-end Geliştirici     |

## 🛠️ Kullanılan Teknolojiler

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (veya varsa Vue/React bilgisi eklenebilir)
- **Veritabanı**: SQLite (geliştirme süreci için)
- **Authentication**: Django Built-in Auth
- **Media/File Uploads**: Django File Storage
- **Bildirim Sistemi**: Django Signals


# 📁 Proje Yapısı (Kısaca)
findora/  
├── accounts/          # Kullanıcı hesaplarıyla ilgili Django uygulaması  
├── findora/          # Ana proje klasörü  
│   ├── settings.py  
│   ├── urls.py  
├── kayip_esya/       # Kayıp eşyalarla ilgili Django uygulaması  
├── media/            # Yüklenen dosyalar  
├── static/           # CSS, JS, resimler  
├── templates/        # Ana şablonlar (index.html gibi)  
├── db.sqlite3        # Veritabanı dosyası  
├── manage.py         # Django yönetim komut dosyası  
└── README.md         # Proje açıklama dosyası  

# ⚙️ Kurulum
Gereksinimler
- Python 3.12
- pip
- virtualenv (önerilir)

## Adımlar
### 1. Repo'yu klonla (Git Bash)
> *git clone* https://github.com/kullaniciadi/findora.git  
> *cd* findora

### 2. Sanal ortam oluştur
> *python -m venv* env  
> **Windows için:** *.\env\Scripts\activate*

### 3. Gereken kütüphaneleri yükle
> *pip install -r* requirements.txt

### 4. Veritabanını oluştur
> *python manage.py migrate*

### 5. Admin oluştur
> *python manage.py createsuperuser*

### 6. Sunucuyu çalıştır
> *python manage.py runserver*

# 📌 Özellikler
- Kullanıcı girişi / kaydı
- Kayıp/bulunan eşya ekleme
- Eşya fotoğrafı yükleme (isteğe bağlı)
- Filtreleme (renk, tür, konum)
- Eşya eşleştirme talebi gönderme
- Yorum yapma

# 🧠 Geliştirilecekler
- 🔍 AI ile fotoğrafa göre eşleşme algoritması
- 🗺️ Harita üzerinden eşya ekleme
- 🔐 Talep doğrulama (dolandırıcılığı önleme mekanizması)
- 📱 Mobil uyumlu tasarım

# 🤝 Katkı
Projeye katkı sağlamak isterseniz:
1.	Fork'layın
2.	Yeni bir branch oluşturun (git checkout -b feature/yenilik)
3.	Commit yapın (git commit -m 'Özellik eklendi')
4.	Push yapın (git push origin feature/yenilik)
5.	Pull Request oluşturun

# 📝 Lisans
Bu proje MIT lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına bakabilirsiniz.
________________________________________
📬 Her türlü geri bildirimi memnuniyetle karşılıyoruz!
