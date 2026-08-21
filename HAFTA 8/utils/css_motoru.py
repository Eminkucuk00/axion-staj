import streamlit as st

def css_ayarlarini_yukle():
    """
    Dashboard'un fütüristik görünümünü (Gradient arka plan, 
    Glassmorphism kartlar, UI gizleme vb.) sağlayan CSS kodlarını enjekte eder.
    """
    
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap');
    
    /* Tüm Uygulamaya Yeni Nesil Font (Outfit) Uygulama */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Material Icons Ayarları */
    .material-symbols-rounded {
      vertical-align: middle;
      margin-right: 5px;
      color: #8b5cf6;
    }

    /* 1. Streamlit Varsayılanlarını Gizleme */
    #MainMenu {display: none !important;}
    footer {display: none !important;}

    /* 2. Hareketli Arka Plan, Sayfa Açılış Animasyonu ve SİBER-GRID */
    .stApp {
        background: linear-gradient(315deg, #05050f 3%, #140428 38%, #08111c 68%, #05050f 98%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite, fadein 1.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        background-attachment: fixed;
    }

    /* Noktalı Veri Ağı (Cyber-Grid) Arka Planı */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
        animation: gridMove 30s linear infinite;
    }
    
    /* Holografik Tarama Çizgisi (Scanline) */
    .stApp::after {
        content: "";
        position: fixed;
        top: -50%; left: 0; width: 100vw; height: 15vh;
        background: linear-gradient(to bottom, transparent, rgba(6, 182, 212, 0.05), transparent);
        pointer-events: none;
        z-index: 9999;
        animation: scanline 10s linear infinite;
    }
    
    .block-container {
        position: relative;
        z-index: 1; /* İçerik gridin üstünde dursun */
    }

    @keyframes gradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    @keyframes fadein {
        from { opacity: 0; transform: translateY(30px); filter: blur(10px); }
        to   { opacity: 1; transform: translateY(0); filter: blur(0px); }
    }
    
    @keyframes gridMove {
        from { transform: translateY(0); }
        to { transform: translateY(40px); }
    }
    
    @keyframes scanline {
        0% { top: -20%; }
        100% { top: 120%; }
    }

    /* 3. Genel Metin Ayarları ve HAREKETLİ NEON BAŞLIKLAR (Gradient Text) */
    h1, h4, h5, h6, p, span, div {
        color: #ffffff;
    }
    
    h2, h3 {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899, #06b6d4);
        background-size: 200% auto;
        color: #fff;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        font-weight: 800 !important;
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* 4. KPI Rakamları (Gümüş/Metalik Gradient) */
    .glass-card h2 {
        background: linear-gradient(135deg, #ffffff, #a78bfa);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 900 !important;
        margin-top: 5px;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    /* 5. Scrollbar (Kaydırma Çubuğu) Özelleştirme */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.5); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #06b6d4; }

    /* 6. Girdi Alanları (Selectbox, Radio vb.) Cam Efekti */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.03) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    div[data-baseweb="select"] > div:hover {
        border: 1px solid #8b5cf6 !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
        transform: scale(1.02);
    }
    
    /* 7. Neon Butonlar (Download ve Genel Butonlar) */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(45deg, #8b5cf6, #ec4899) !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    }
    [data-testid="baseButton-primary"]:hover {
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.8) !important;
        transform: translateY(-3px) scale(1.02);
    }

    /* ========================================================= */
    /* 🚀 ULTIMATE NEON "WOW" MODU (MAKSİMUM GÖSTERİŞ) 🚀 */
    /* ========================================================= */

    /* 1. HAREKETLİ NEON UZAY ARKA PLANI */
    .stApp {
        background: linear-gradient(315deg, #0f0c29, #302b63, #24243e, #0f0c29) !important;
        background-size: 400% 400% !important;
        animation: neon-bg 15s ease infinite !important;
        background-attachment: fixed !important;
    }
    
    @keyframes neon-bg {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* Noktalı Lazer Ağı (Cyber-Grid) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: radial-gradient(rgba(6, 182, 212, 0.2) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
        animation: gridMove 20s linear infinite;
    }

    /* 2. NEON CAM KARTLAR (3D Tilt & Lazer Gölgeler) */
    .glass-card {
        background: rgba(20, 10, 40, 0.6);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 1px solid rgba(6, 182, 212, 0.5);
        border-bottom: 1px solid rgba(236, 72, 153, 0.5);
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(139, 92, 246, 0.1);
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        position: relative;
        z-index: 1;
    }
    
    .glass-card:hover {
        transform: perspective(1000px) rotateX(5deg) rotateY(5deg) translateY(-10px) scale(1.05);
        border-color: #06b6d4;
        box-shadow: -15px 25px 50px rgba(6, 182, 212, 0.4), 15px -25px 50px rgba(236, 72, 153, 0.4);
    }

    /* 3. ÇILDIRMIŞ NEON TİPOGRAFİ (Yazıların İçinde Dönen Renkler) */
    .glass-card h4 {
        color: #e2e8f0;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .glass-card h2, h2, h3 {
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899, #06b6d4) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 900 !important;
        animation: shine 3s linear infinite !important;
        text-shadow: 0px 5px 15px rgba(139, 92, 246, 0.3);
    }
    
    .glass-card h2 { font-size: 3.5rem !important; margin: 10px 0; }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* 4. LAZER İNDİRME BUTONU (Glowing Edge) */
    [data-testid="baseButton-primary"] {
        background: linear-gradient(45deg, #06b6d4, #8b5cf6, #ec4899) !important;
        background-size: 200% 200% !important;
        border: none !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 15px 30px !important;
        animation: neon-bg 3s ease infinite !important;
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.6) !important;
        transition: all 0.2s !important;
    }
    
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 0 40px rgba(6, 182, 212, 0.9), 0 0 40px rgba(236, 72, 153, 0.9) !important;
    }
    
    /* 5. UÇAN GRAFİKLER VE NEON TABLOLAR */
    .js-plotly-plot {
        transition: all 0.4s ease;
    }
    .js-plotly-plot:hover {
        transform: translateY(-5px) scale(1.02);
        filter: drop-shadow(0px 20px 30px rgba(139, 92, 246, 0.5));
    }
    
    div[data-testid="stDataFrame"] {
        border-radius: 15px;
        border: 2px solid rgba(6, 182, 212, 0.5);
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.3), inset 0 0 10px rgba(236, 72, 153, 0.2);
        transition: all 0.3s ease;
    }
    div[data-testid="stDataFrame"]:hover {
        border-color: #ec4899;
        box-shadow: 0 0 30px rgba(236, 72, 153, 0.6);
    }

    /* 6. Sidebar (Neon Çizgili Koyu Cam) */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 12, 41, 0.7) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 2px solid rgba(139, 92, 246, 0.4);
        box-shadow: 5px 0 30px rgba(139, 92, 246, 0.2);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
