import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3

# ============================================
# SAYFA AYARLARI
# ============================================
st.set_page_config(
    page_title="🎤 Diksiyon Pro",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS STİLLERİ
# ============================================
st.markdown("""
    <style>
    :root {
        --primary: #667eea;
        --success: #48bb78;
        --danger: #f56565;
        --warning: #ed8936;
        --dark: #1a202c;
    }
    
    .main {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2em;
    }
    
    .card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 153, 255, 0.1));
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    .streak-info {
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE BAŞLATMA
# ============================================
if 'users' not in st.session_state:
    st.session_state.users = [
        {
            'id': 1,
            'name': 'Demo Kullanıcı',
            'email': 'test@test.com',
            'password': 'MTIzNDU2',  # base64 encoded: 123456
            'phone': '05XX XXX XXXX',
            'createdDate': datetime.now().isoformat()
        }
    ]

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'words' not in st.session_state:
    st.session_state.words = []

if 'exercises' not in st.session_state:
    st.session_state.exercises = []

if 'streak_days' not in st.session_state:
    st.session_state.streak_days = 0

if 'last_exercise_date' not in st.session_state:
    st.session_state.last_exercise_date = None

if 'completed_exercises' not in st.session_state:
    st.session_state.completed_exercises = {}

if 'selected_word_ids' not in st.session_state:
    st.session_state.selected_word_ids = set()

# ============================================
# EGZERSİZLER VERİSİ
# ============================================
EXERCISES = [
    {
        "id": 1,
        "name": "🫁 Diyafram Nefesi",
        "duration": 300,
        "description": "Diyafram kontrolü, konuşma hacmi ve nefes desteği",
        "steps": [
            "Derin nefes al (4 saniye, diyaframa odaklan - göbeğin şişmeli, göğsün değil)",
            "Rahat otur, omuzlarını aşağıya çek, sırt düz",
            "Ağzından tamamen hava ver (4-5 saniye, fışsss sesini çıkar)",
            "Burnundan 4 sayarak hava al (diyafram aşağı insin, göbeğin çıksın)",
            "4 sayarak hava tut",
            "6 sayarak yavaş hava ver",
            "Bunu 5-10 kez tekrarla, her gün 2-3 dakika"
        ],
        "benefits": [
            "✅ Nefes kontrol ve stabilizasyonu",
            "✅ Ses yüksekliği ve ton kontrolü",
            "✅ Uzun cümleler rahatça söyleyebilme"
        ]
    },
    {
        "id": 2,
        "name": "🔊 Güç Nefesi - Hava Akışı",
        "duration": 240,
        "description": "Uzun cümleleri rahatça söyleyebilme ve nefes bitme sorunu çözme",
        "steps": [
            "Ayakta dur, bacakların omuz genişliğinde açık, dik dur",
            "Derin nefes al (4 saniye, diyaframa odaklan)",
            "Mum söyler gibi nefes ver (ffff - yavaş, kontrollü)",
            "Nefesi uzat, 20-30 saniye hedefle",
            "Nefes bittiğinde hemen yeni nefes al",
            "10-15 kez tekrarla, nefes bitiş zamanını kademeli arttır"
        ],
        "benefits": [
            "✅ Konuşma dayanıklılığı",
            "✅ Uzun cümleleri kesintisiz söyleyebilme",
            "✅ Hava akış kontrolü"
        ]
    },
    {
        "id": 3,
        "name": "🎯 4-7-8 Sakinleştirme Nefesi",
        "duration": 180,
        "description": "Heyecan yönetimi ve ses kontrolü",
        "steps": [
            "Rahat otur veya uzun şekilde yat",
            "4 sayarak derin nefes al (burnundan)",
            "7 sayarak nefesi tut",
            "8 sayarak daha uzun sürede hava ver (ağızdan)",
            "3-4 kez tekrarla, sunumdan 5 dakika önce yap",
            "Heyecan anında kendini sakinleştirmeye kullan"
        ],
        "benefits": [
            "✅ Heyecan ve endişe azaltma",
            "✅ Sinir sistemi sakinleştirme",
            "✅ Konuşma sırasında rahatlık"
        ]
    },
    {
        "id": 4,
        "name": "🗣️ Gırtlak Gevşetme",
        "duration": 200,
        "description": "Ses kalitesi iyileştirme ve gırtlak gerilimi çözme",
        "steps": [
            "Rahat sesle 'ng' sesini çıkar (ıng, ang, ung sesleriyle)",
            "Sesini düşük başlat, yavaş yükselt, sonra düşür",
            "Her vokal (A, E, I, O, U) ile bunu tekrarla",
            "10 kez tekrarla, her gün yapılması tavsiye edilir"
        ],
        "benefits": [
            "✅ Boğuk ses giderme",
            "✅ Gırtlak rahatlatma",
            "✅ Ses kalitesi gelişimi"
        ]
    },
    {
        "id": 5,
        "name": "🎤 Rezonans Odası Egzersizi",
        "duration": 220,
        "description": "Ses gücü ve resonanssı artırma",
        "steps": [
            "Burun üzerinde hafif masaj yap (titreşim hisset)",
            "'Mmmm' sesi çıkar, burunda titreşim hissedin",
            "Sonra 'Maaa, Meee, Miii, Mooo, Muuu' söyle",
            "Dudaklarını serbest bırak (Pppp sesinden başlayıp Baaa'ya geç)",
            "Her harf için 5-6 kez tekrarla"
        ],
        "benefits": [
            "✅ Sesinin gücü ve tonu iyileştirme",
            "✅ Daha dolgun ve etkileyici ses",
            "✅ Profesyonel ses kalitesi"
        ]
    },
    {
        "id": 6,
        "name": "🎵 Tonlama Alıştırması",
        "duration": 250,
        "description": "Duygusal konuşma ve anlamsal vurgu",
        "steps": [
            "Aynı cümleyi farklı duygularla söyle: 'Teşekkür ederim'",
            "Düz (Neutral): Teşekkür ederim",
            "Heyecanlı: Teşekkür ederim!",
            "Sorulu: Teşekkür mı ettim?",
            "Her duygusal versiyonu 3-4 kez tekrarla"
        ],
        "benefits": [
            "✅ Aynı cümleyi farklı anlamlarla söyleyebilme",
            "✅ Konuşmanın etkisini 10 kat artırma",
            "✅ Konuşmanızı daha canlı hale getirme"
        ]
    },
    {
        "id": 7,
        "name": "👄 Dudak Kasları - Net Sesi",
        "duration": 180,
        "description": "B, P, V, M seslerinin net çıkması",
        "steps": [
            "Dudaklarını sıkıp gevşet (10 kez, hızlı)",
            "Dudak uçlarını sıkı kırış (5 saniye tut, 5 kez)",
            "'O' → 'A' arasında gidip gel (10 kez)",
            "Dudaklarını şişir, 3 saniye tut, hava ver (5 kez)",
            "Dudaklarını titret: 'Brrrrr' sesi (10 saniye)",
            "Hızlı bir şekilde: Ba-ba-ba, Pa-pa-pa, Va-va-va, Ma-ma-ma söyle"
        ],
        "benefits": [
            "✅ B, P, V, M seslerinin netliği",
            "✅ İfade gücü artışı",
            "✅ Net konuşma"
        ]
    },
    {
        "id": 8,
        "name": "👅 Dil Çevikliği - Hız",
        "duration": 200,
        "description": "T, D, L, N, R seslerinin netliği ve konuşma hızı",
        "steps": [
            "Dil uçunu üst dişlere değdir, titreştir (20 kez, Rrrr sesi)",
            "Dili yanına basarken sesi çıkar (sağ-sol, 15 kez)",
            "Dil uçunu çıkart → içeri al (10 kez, hızlı)",
            "Dili ağız içinde daire çizdir (5 tur)",
            "Hızlı: 'Ta-ta-ta' → 'Da-da-da' → 'La-la-la' (20 kez)"
        ],
        "benefits": [
            "✅ T, D, L, N, R seslerinin mükemmel net çıkması",
            "✅ Konuşma hızının kontrolü",
            "✅ Mental aktivite artışı"
        ]
    },
    {
        "id": 9,
        "name": "😮 Çene & Ağız Açıklığı",
        "duration": 190,
        "description": "Geniş ağız açıklığı ve doğal konuşma",
        "steps": [
            "Çeneyi rahatça aç-kapat (10 kez, doğal)",
            "Çeneyi sağa-sola hareket ettir (8 kez her yön)",
            "Çeneyi daire çize çize hareket ettir (saat yönünde 8 kez)",
            "Ağzı açık, çeneyi aşağı doğru pes (3 saniye, 5 kez)",
            "Geniş ağız açıklığıyla: 'Ah-Eh-Ih-Oh-Uh' söyle (10 kez)"
        ],
        "benefits": [
            "✅ Geniş ağız açıklığı daha dolu ses sağlar",
            "✅ Tüm vokalleri açık ve net çıkarma",
            "✅ Doğal konuşma ritmi"
        ]
    },
    {
        "id": 10,
        "name": "📖 Yüksek Sesle Okuma",
        "duration": 600,
        "description": "Ritim, akıcılık ve doğal hız kontrolü",
        "steps": [
            "Rahat bir kitap veya makale seç",
            "Nefes egzersizleri yap (2 dakika)",
            "Yavaş ve açık bir şekilde okumaya başla (5 dakika)",
            "Hızını kademeli olarak arttır (2 dakika)",
            "Metnin anlamını vurgularla aktarma (1 dakika)"
        ],
        "benefits": [
            "✅ Cümle yapısını anlama",
            "✅ Akıcı ve sürüklü konuşma",
            "✅ Anlamlı ve etkili konuşma"
        ]
    },
    {
        "id": 11,
        "name": "💬 Doğaçlama Konuşma",
        "duration": 600,
        "description": "Hazırlanmamış konuşma ve spontane ifade",
        "steps": [
            "Haftalık temalar belirle (siyaset, eğitim, spor vb.)",
            "Konuyu başlamanın 10 saniyesi içinde söylemeye başla",
            "Hazırlanmadan 2-3 dakika konuş",
            "Haftada 2-3 kez farklı konularda praktik yap"
        ],
        "benefits": [
            "✅ Hazırlanmamış konuşmada rahat olma",
            "✅ Heyecan yönetimi",
            "✅ Kendinden emin konuşma"
        ]
    },
    {
        "id": 12,
        "name": "📣 Anlatım Egzersizi",
        "duration": 600,
        "description": "Hikaye anlatımı ve etkili iletişim",
        "steps": [
            "Şahsi bir hikaye veya örnek seç",
            "Ana noktaları not et (başlangıç, çatışma, çözüm)",
            "Dikkat çekici açılış yap (soru veya sürpriz)",
            "Heyecanı kademeli arttır",
            "Zirve noktasında sesini ve hızını kontrol et"
        ],
        "benefits": [
            "✅ İnsanları duygusal olarak bağlama",
            "✅ Liderlik ve etkileme yeteneği",
            "✅ Kalıcı iletişim"
        ]
    },
    {
        "id": 13,
        "name": "🎭 Tekerleme Egzersizi",
        "duration": 300,
        "description": "Dil çevikliği, artikülasyon ve tempo kontrolü",
        "steps": [
            "Konfor seviyesi düşük bir tekerleme seç",
            "Yavaş bir tempo ile diksiyon üzerine odaklan",
            "Tempoyu kademeli arttır",
            "Normal hızda tekrarla (5 dakika)",
            "Hızını arttır ve net konuşma kalitesini koru"
        ],
        "benefits": [
            "✅ Dil çevikliği ve kontrolü",
            "✅ Ses açıklığı ve netlik",
            "✅ Hafıza güçlenmesi"
        ]
    }
]

# ============================================
# NAVBAR (HEADER)
# ============================================
col1, col2, col3 = st.columns([3, 5, 2])
with col1:
    st.markdown("# 🎤 Diksiyon Pro")

with col3:
    if st.session_state.current_user:
        st.markdown(f"### 👋 {st.session_state.current_user['name']}")
        if st.button("🚪 Çıkış Yap"):
            st.session_state.current_user = None
            st.rerun()

# ============================================
# GİRİŞ / KAYIT
# ============================================
if not st.session_state.current_user:
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Giriş Yap", "📝 Üye Ol", "🔑 Şifre Sıfırla"])
    
    with tab1:
        st.markdown("## Giriş Yapın")
        st.info("💡 **Demo Hesap:** test@test.com / 123456")
        
        login_email = st.text_input("📧 E-posta", key="login_email")
        login_password = st.text_input("🔐 Şifre", type="password", key="login_password")
        
        if st.button("Giriş Yap", key="login_btn"):
            import base64
            user = next((u for u in st.session_state.users 
                        if u['email'] == login_email 
                        and u['password'] == base64.b64encode(login_password.encode()).decode()),
                       None)
            
            if user:
                st.session_state.current_user = user
                st.success(f"✅ Hoş geldin, {user['name']}!")
                st.rerun()
            else:
                st.error("❌ E-posta veya şifre hatalı!")
    
    with tab2:
        st.markdown("## Üye Olun")
        
        reg_name = st.text_input("👤 Ad-Soyad", key="reg_name")
        reg_phone = st.text_input("📱 Telefon", key="reg_phone")
        reg_email = st.text_input("📧 E-posta", key="reg_email")
        reg_password = st.text_input("🔐 Şifre (min 6 karakter)", type="password", key="reg_password")
        
        if st.button("Üye Ol", key="register_btn"):
            if not all([reg_name, reg_phone, reg_email, reg_password]):
                st.error("❌ Tüm alanları doldurun!")
            elif len(reg_password) < 6:
                st.error("❌ Şifre en az 6 karakter olmalı!")
            elif any(u['email'] == reg_email for u in st.session_state.users):
                st.error("❌ Bu e-posta zaten kayıtlı!")
            else:
                import base64
                new_user = {
                    'id': len(st.session_state.users) + 1,
                    'name': reg_name,
                    'email': reg_email,
                    'password': base64.b64encode(reg_password.encode()).decode(),
                    'phone': reg_phone,
                    'createdDate': datetime.now().isoformat()
                }
                st.session_state.users.append(new_user)
                st.success("✅ Üyeliğiniz oluşturuldu! Giriş yapabilirsiniz.")
    
    with tab3:
        st.markdown("## Şifre Sıfırla")
        forgot_email = st.text_input("📧 E-posta Adresiniz")
        
        if st.button("Gönder"):
            user = next((u for u in st.session_state.users if u['email'] == forgot_email), None)
            if user:
                st.success("✅ Yeni şifreniz gösterilecektir (demo sürümde)")
                st.info(f"Yeni şifreniz: temp12345")
            else:
                st.warning("⚠️ Bu e-posta sistemde bulunamadı.")

else:
    # ============================================
    # ANA ARAYÜZ (LOGIN SONRASI)
    # ============================================
    
    tab_dashboard, tab_exercises, tab_words, tab_stats, tab_profile = st.tabs(
        ["📊 Dashboard", "🎯 Egzersizler", "📚 Kelimeler", "📈 İstatistikler", "👤 Profil"]
    )
    
    # ============================================
    # DASHBOARD
    # ============================================
    with tab_dashboard:
        st.markdown("## 🎉 Hoş Geldin!")
        st.markdown("Bugünün egzersizine başlamak için **Egzersizler** sekmesini ziyaret et.")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <h3>📅 Bugünkü Dakika</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <h3>⏰ Haftalık Egzersiz</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='stat-card'>
                <h3>📖 Öğrenilen Kelime</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class='stat-card'>
                <h3>🏆 Toplam Dakika</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================
    # EGZERSIZLER
    # ============================================
    with tab_exercises:
        st.markdown("## 🎯 Egzersiz Programı")
        st.markdown("Tüm egzersizleri yaparak diksiyon ve konuşma becerini geliştir!")
        
        for exercise in EXERCISES:
            with st.expander(f"{exercise['name']} - {exercise['duration']}s"):
                st.markdown(f"**{exercise['description']}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📋 Nasıl Yapılır:")
                    for i, step in enumerate(exercise['steps'], 1):
                        st.markdown(f"{i}. {step}")
                
                with col2:
                    st.markdown("### ✨ Kazandığı Faydalar:")
                    for benefit in exercise['benefits']:
                        st.markdown(benefit)
                
                if st.button(f"▶ {exercise['name']} ile Başla", key=f"exercise_{exercise['id']}"):
                    st.session_state.current_exercise = exercise['id']
                    st.success(f"✅ {exercise['name']} başladı!")
    
    # ============================================
    # KELIMELER
    # ============================================
    with tab_words:
        st.markdown("## 📚 Kelime Yönetimi")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Kelime Ekle"):
                st.session_state.show_word_form = True
        
        with col2:
            if st.button("📤 CSV Yükle"):
                st.session_state.show_csv_upload = True
        
        with col3:
            if st.button("⬇️ CSV İndir"):
                if st.session_state.words:
                    df = pd.DataFrame(st.session_state.words)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 İndir",
                        data=csv,
                        file_name="kelimeler.csv",
                        mime="text/csv"
                    )
        
        st.markdown("---")
        
        # Kelime Ekleme Formu
        if st.session_state.get('show_word_form', False):
            with st.form("word_form"):
                st.markdown("### ➕ Yeni Kelime Ekle")
                word = st.text_input("Kelime")
                pronunciation = st.text_input("Okunuşu")
                meaning = st.text_area("Anlamı")
                difficulty = st.selectbox("Zorluk", ["🟢 Kolay", "🟡 Orta", "🔴 Zor"])
                
                if st.form_submit_button("Kaydet"):
                    if all([word, pronunciation, meaning]):
                        new_word = {
                            'id': len(st.session_state.words) + 1,
                            'word': word,
                            'pronunciation': pronunciation,
                            'meaning': meaning,
                            'difficulty': difficulty,
                            'status': 'learning',
                            'dateAdded': datetime.now().isoformat()
                        }
                        st.session_state.words.append(new_word)
                        st.session_state.show_word_form = False
                        st.success("✅ Kelime eklendi!")
                        st.rerun()
                    else:
                        st.error("❌ Tüm alanları doldurun!")
        
        # Kelimeleri Listele
        st.markdown("### 📚 Kelime Listesi")
        
        if st.session_state.words:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**📖 Toplam:** {len(st.session_state.words)}")
            with col2:
                learned = len([w for w in st.session_state.words if w['status'] == 'learned'])
                st.markdown(f"**✅ Öğrenildi:** {learned}")
            with col3:
                learning = len([w for w in st.session_state.words if w['status'] == 'learning'])
                st.markdown(f"**🔄 Öğreniliyor:** {learning}")
            
            st.markdown("---")
            
            df = pd.DataFrame(st.session_state.words)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📚 Henüz kelime eklenmedi.")
    
    # ============================================
    # İSTATİSTİKLER
    # ============================================
    with tab_stats:
        st.markdown("## 📈 İstatistikler")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📅 Günlük"):
                st.session_state.stat_period = 'daily'
        with col2:
            if st.button("📆 Haftalık"):
                st.session_state.stat_period = 'weekly'
        with col3:
            if st.button("📋 Aylık"):
                st.session_state.stat_period = 'monthly'
        with col4:
            if st.button("🏆 Tümü"):
                st.session_state.stat_period = 'all'
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <h3>✅ Yapılan Egzersiz</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <h3>⏱️ Toplam Dakika</h3>
                <h2>0</h2>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================
    # PROFIL
    # ============================================
    with tab_profile:
        st.markdown("## 👤 Profilim")
        
        user = st.session_state.current_user
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"## {user['name'][0].upper()}")
        
        with col2:
            st.markdown(f"### {user['name']}")
            st.markdown(f"📧 {user['email']}")
            st.markdown(f"📱 {user['phone']}")
            st.markdown(f"📅 Kayıt: {user['createdDate'][:10]}")
        
        st.markdown("---")
        
        st.markdown("### ⚠️ Tehlikeli Bölge")
        st.warning("Egzersiz geçmişinizi ve istatistiklerinizi sıfırlamak istiyorsanız:")
        
        if st.button("⚠️ Tüm İlerlememi Sıfırla", key="reset_progress"):
            st.session_state.exercises = []
            st.session_state.streak_days = 0
            st.session_state.completed_exercises = {}
            st.session_state.words = [
                {**w, 'status': 'learning'} 
                for w in st.session_state.words
            ]
            st.success("✅ Tüm ilerlemeniz sıfırlandı.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🎤 Diksiyon Pro | Streamlit with ❤️ | 
    <a href='https://github.com' target='_blank'>GitHub Deposu</a>
</div>
""", unsafe_allow_html=True)