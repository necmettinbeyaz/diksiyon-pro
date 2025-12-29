# 🚀 GitHub ve Streamlit Cloud Yayınlama Rehberi

## Adım 1: GitHub Deposu Oluştur

### 1.1 GitHub Hesabına Giriş
1. https://github.com/new adresine git
2. Giriş yap veya kayıt ol

### 1.2 Yeni Depo Oluştur
- **Repository name:** `diksiyon-pro`
- **Description:** Türkçe diksiyon ve ses kalitesi geliştirme uygulaması
- **Public** seçin (Streamlit Cloud erişimi için)
- **.gitignore:** Python seç
- **License:** MIT seç
- **Create repository** butonuna tıkla

---

## Adım 2: Dosyaları Yükle

### Windows (CMD veya PowerShell)

```bash
# 1. Depo klasörünü oluştur
mkdir diksiyon-pro
cd diksiyon-pro

# 2. Git başlat
git init
git config user.name "Adın"
git config user.email "email@example.com"

# 3. Dosyaları kopyala (şu dosyaları ekle)
# - app.py
# - requirements.txt
# - README.md
# - .gitignore
# - config.toml

# 4. GitHub bağlantısını ekle
git remote add origin https://github.com/YOUR-USERNAME/diksiyon-pro.git

# 5. Değişiklikleri stage et
git add .

# 6. Commit et
git commit -m "Diksiyon Pro Streamlit uygulaması başlangıç"

# 7. GitHub'a gönder
git branch -M main
git push -u origin main
```

### Mac/Linux

```bash
# Aynı komutlar, ancak:
mkdir -p ~/diksiyon-pro
cd ~/diksiyon-pro
```

---

## Adım 3: Streamlit Cloud'da Deploy

### 3.1 Streamlit Share Hesabı Oluştur
1. https://share.streamlit.io adresine git
2. "Sign in with GitHub" butonuna tıkla
3. GitHub hesabını yetkilendir

### 3.2 Yeni Uygulamayı Deploy Et

1. **Streamlit Cloud Dashboard**'da "New app" butonuna tıkla
2. Aşağıdaki seçenekleri ayarla:
   - **Repository:** `YOUR-USERNAME/diksiyon-pro`
   - **Branch:** `main`
   - **Main file path:** `app.py`

3. **Deploy!** butonuna tıkla
4. Uygulamanın derlenmiş olmasını bekle (~2-3 dakika)

### 3.3 Uygulamaya Erişim

Deployment tamamlandığında, otomatik bir URL oluşturulur:
```
https://diksiyon-pro-YOUR-USERNAME.streamlit.app
```

---

## Adım 4: Güncellemeleri Gönder

Kodunda değişiklik yaptığında:

```bash
# 1. Değişiklikleri stage et
git add .

# 2. Commit et
git commit -m "Açıklama yaz"

# 3. GitHub'a gönder
git push origin main
```

Streamlit Cloud otomatik olarak algılayacak ve yeniden deploy edecek (~1-2 dakika).

---

## 📋 Dosya Kontrol Listesi

GitHub deposunda bu dosyalar olmalı:

```
diksiyon-pro/
├── app.py                    ✅ Ana uygulamasi
├── requirements.txt          ✅ Bağımlılıklar
├── README.md                 ✅ Belgelendirme
├── .gitignore               ✅ Git ignore kuralları
├── DEPLOYMENT.md            ✅ Bu dosya
└── .streamlit/
    └── config.toml          ✅ Streamlit ayarları
```

---

## 🔧 Sorun Giderme

### Deploy başarısız oldu?

**Hata:** `ModuleNotFoundError: No module named 'X'`

**Çözüm:** `requirements.txt` dosyasında eksik paket var.

```bash
# Örnek:
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Requirements güncellendi"
git push origin main
```

### Uygulama yavaş?

**Çözüm:** Streamlit Cloud'da sınırlı kaynaklar var. Optimizasyon yapın:
- Veri setini küçültün
- Gereksiz işlemleri kaldırın
- @st.cache decorator'ı kullanın

### GitHub bağlantısı olmadı?

**Çözüm:**
1. SSH key oluştur:
   ```bash
   ssh-keygen -t ed25519 -C "email@example.com"
   ```

2. Public key'i GitHub'a ekle:
   - Settings → SSH and GPG keys → New SSH key
   - Dosya: `~/.ssh/id_ed25519.pub` içeriğini kopyala

3. HTTPS yerine SSH kullan:
   ```bash
   git remote set-url origin git@github.com:YOUR-USERNAME/diksiyon-pro.git
   ```

---

## 🌐 Custom Domain (Opsiyonel)

Streamlit Cloud'da custom domain eklemek için:

1. Streamlit Cloud account settings'e git
2. "Custom domains" bölümüne git
3. Domain ekle (DNS ayarları gerekli)

---

## 📊 Analitik ve Monitoring

### Streamlit Cloud Metrics
- App views
- Load times
- Error logs

Settings → View logs adresinden izleyebilirsin.

---

## 💬 İhtiyaç Duyulabilecek Bilgiler

- **GitHub Username:** `YOUR-USERNAME` yerine yazacaksın
- **GitHub Email:** Git config'te kullanacaksın
- **Streamlit Email:** Streamlit hesabı oluşturmada

---

## 🎉 Başarılı Deployment!

Eğer başarıyla deploy ettiysen:

✅ Uygulamana https://diksiyon-pro-YOUR-USERNAME.streamlit.app adresinden erişebilirsin
✅ Güncellemeleri otomatik olarak deploy edilecek
✅ Sorunları Streamlit logs'tan görebilirsin
✅ Kullanıcılar uygulamayı kullanmaya başlayabilir

---

## 📚 Yardımcı Linkler

- [Streamlit Documentation](https://docs.streamlit.io)
- [GitHub Guides](https://guides.github.com)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

**İyi Çalışmalar! 🎤**
