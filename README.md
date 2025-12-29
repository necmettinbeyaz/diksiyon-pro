# 🎤 Diksiyon Pro - Streamlit Versiyonu

Türkçe konuşma, diksiyon ve ses kalitesini geliştirmek için yapılmış etkileşimli bir uygulamadır.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ Özellikler

### 🎯 13 Farklı Egzersiz
- 🫁 Diyafram Nefesi
- 🔊 Güç Nefesi
- 🎯 4-7-8 Sakinleştirme Nefesi
- 🗣️ Gırtlak Gevşetme
- 🎤 Rezonans Odası
- 🎵 Tonlama Alıştırması
- 👄 Dudak Kasları
- 👅 Dil Çevikliği
- 😮 Çene & Ağız Açıklığı
- 📖 Yüksek Sesle Okuma
- 💬 Doğaçlama Konuşma
- 📣 Anlatım Egzersizi
- 🎭 Tekerleme Egzersizi

### 📚 Kelime Yönetimi
- ✏️ Kelime ekleme ve düzenleme
- 📤 CSV'den toplu kelime yükleme
- 📊 İstatistikler ve ilerleme takibi
- 🎮 Spaced Repetition oyunu
- 🔊 Profesyonel seslendirime

### 👥 Kullanıcı Yönetimi
- 📝 Üyelik sistemi
- 🔐 Şifre sıfırlama
- 📊 Kişisel istatistikler
- 🏆 Günlük seriler

### 📊 Analitik
- 📈 Haftalık/aylık istatistikler
- 🎯 Egzersiz takibi
- 📚 Kelime öğrenme ilerlemesi
- 🔥 Motivasyon serileri

---

## 🚀 Kurulum

### Yerel Çalıştırma

1. **Depoyu klonla:**
```bash
git clone https://github.com/yourusername/diksiyon-pro.git
cd diksiyon-pro
```

2. **Sanal ortam oluştur:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Bağımlılıkları yükle:**
```bash
pip install -r requirements.txt
```

4. **Uygulamayı çalıştır:**
```bash
streamlit run app.py
```

5. **Tarayıcıda aç:**
```
http://localhost:8501
```

---

## 🌐 Streamlit Cloud'da Yayınlama

### Adım 1: GitHub'a Gönder

```bash
git add .
git commit -m "Diksiyon Pro Streamlit uygulaması"
git push origin main
```

### Adım 2: Streamlit Cloud

1. https://share.streamlit.io adresine git
2. GitHub hesabını bağla
3. Depoyu seç: `yourusername/diksiyon-pro`
4. Ana dosyayı ayarla: `app.py`
5. **Deploy** butonuna tıkla

### Adım 3: Kişisel Alan Adı (Opsiyonel)

Streamlit Cloud ayarlarından custom domain ekleyebilirsin.

---

## 📖 Kullanım

### Demo Hesap
- **E-posta:** test@test.com
- **Şifre:** 123456

### Kelime Ekleme
1. "📚 Kelimeler" sekmesine git
2. "➕ Kelime Ekle" butonuna tıkla
3. Kelimeyi, okunuşunu ve anlamını gir
4. Zorluk seviyesini seç
5. Kaydet

### Egzersiz Yapma
1. "🎯 Egzersizler" sekmesine git
2. İstediğin egzersizi seç
3. Detaylı talimatları oku
4. "▶ Başla" butonuna tıkla
5. Zaman sayıcı otomatik başlayacak

### İstatistikleri İzle
1. "📈 İstatistikler" sekmesine git
2. Zaman aralığını seç (günlük/haftalık/aylık/tümü)
3. İlerlemenizi görün

---

## 📁 Dosya Yapısı

```
diksiyon-pro/
├── app.py              # Ana Streamlit uygulaması
├── requirements.txt    # Python bağımlılıkları
├── README.md          # Bu dosya
├── .gitignore         # Git ignore kuralları
└── .streamlit/
    └── config.toml    # Streamlit ayarları
```

---

## 🔧 Yapılandırma

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
```

---

## 🎓 Egzersizler Hakkında

Her egzersiz bilimsel olarak tasarlanmıştır:

### Diyafram Nefesi
- **Süre:** 5 dakika
- **Fayda:** Nefes kontrolü, ses yüksekliği
- **Frekans:** Günde 2-3 kez

### Tekerleme Egzersizi
- **Süre:** 5 dakika
- **Fayda:** Dil çevikliği, diksiyon netliği
- **Frekans:** Günde 1 kez

### Tonlama Alıştırması
- **Süre:** 4-5 dakika
- **Fayda:** Duygusal ifade, anlamsal vurgu
- **Frekans:** Haftada 3-4 kez

---

## 💻 Geliştirme

### Yeni Egzersiz Ekleme

`app.py` dosyasında `EXERCISES` listesine yeni egzersiz ekle:

```python
{
    "id": 14,
    "name": "🆕 Yeni Egzersiz",
    "duration": 300,
    "description": "Açıklama",
    "steps": [
        "1. Adım",
        "2. Adım",
        "3. Adım"
    ],
    "benefits": [
        "✅ Fayda 1",
        "✅ Fayda 2"
    ]
}
```

### Yeni Özellik Ekleme

1. Fork et
2. Feature branch oluştur (`git checkout -b feature/YeniOzellik`)
3. Değişiklikleri yap
4. Commit et (`git commit -am 'Yeni özellik eklendi'`)
5. Push et (`git push origin feature/YeniOzellik`)
6. Pull Request aç

---

## 🐛 Bilinen Sorunlar

- Seslendirime Safari'de sınırlı
- CSV yükleme büyük dosyalarda yavaş olabilir
- Offline modda sessiz video yayını çalışmayabilir

---

## 📞 İletişim

- **E-posta:** support@diksiyon-pro.com
- **GitHub Issues:** [Sorun Bildir](https://github.com/yourusername/diksiyon-pro/issues)
- **Twitter:** [@Diksiyon_Pro](https://twitter.com)

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasını gör.

---

## 🙏 Katkıda Bulunanlar

- Herkes katkı yapabilir!
- Kod kalitesi önemlidir
- Testler yazınız
- Belgelendirmeyi güncelleyin

---

## 🎯 Gelecek Planlar

- [ ] Google Cloud TTS entegrasyonu
- [ ] Mobil uygulama (React Native)
- [ ] Yapay zeka tabanlı geri bildirim
- [ ] Topluluk forumu
- [ ] Premium üyelik seçenekleri
- [ ] Video tutorial'lar
- [ ] İngilizce, Arapça dil desteği

---

**🎤 Diksiyon Pro ile konuşmanızı geliştirin!**

Yapılan son güncellemeler için [Changelog](CHANGELOG.md) dosyasını kontrol et.
