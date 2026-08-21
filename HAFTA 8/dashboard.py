import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import requests

from utils.veri_islemleri import veri_yukle, veriyi_filtrele, association_rules_hesapla
from utils.css_motoru import css_ayarlarini_yukle
from utils.kpi_hesaplayici import kpi_hesapla
from utils.gorsellestirme import (
    ciz_en_cok_satanlar, ciz_gercek_sadakat, 
    ciz_heatmap, ciz_sepet_buyuklugu, ciz_network_graph
)

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Instacart AI Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS ve UI Ayarları (Glassmorphism & Animasyonlar)
css_ayarlarini_yukle()

from datetime import date

karsilama_html = """<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

#rk-print, #rk-close{ position:absolute; width:1px; height:1px; opacity:0; overflow:hidden; }

/* Fiş kesilene kadar sidebar'ı (Filtreler) Streamlit'in hatırladığı duruma bakmaksızın zorla gizle */
[data-testid="stSidebar"]{ display:none !important; }
body.rk-unlocked [data-testid="stSidebar"]{ display:block !important; }
/* Streamlit'in kendi aç/kapa okunu her zaman görünür bırakıyoruz: JS'imiz çalışmazsa
   kullanıcı elle tıklayıp sidebar'ı açabilsin (bu durumda Streamlit aria-expanded="true" yapar) */
[data-testid="stSidebar"][aria-expanded="true"]{ display:block !important; }

#rk-modal{
  position:fixed; inset:0; z-index:9999999;
  display:flex; align-items:flex-start; justify-content:center;
  padding:6vh 16px 40px;
  overflow-y:auto;
  background:radial-gradient(ellipse at 50% 15%, #17231d 0%, #070a08 68%);
  font-family:'Space Mono', monospace;
  transition:opacity .45s ease, visibility 0s .45s;
}
#rk-close:checked ~ #rk-modal{ opacity:0; visibility:hidden; pointer-events:none; }

.rk-stage{ display:flex; flex-direction:column; align-items:center; }

/* --- tıklanabilir "fiş yazdır" butonu --- */
.rk-print-btn{
  display:flex; flex-direction:column; align-items:center; gap:12px;
  width:min(240px,72vw); padding:22px 20px 24px;
  background:linear-gradient(180deg,#37473c,#1a211c);
  border:1px solid rgba(255,255,255,.09);
  border-radius:18px;
  cursor:pointer; user-select:none;
  box-shadow:0 22px 45px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);
  animation:rk-pulse-ring 2.4s ease-in-out infinite;
  transition:opacity .4s ease, transform .4s ease, margin .4s ease;
}
.rk-print-btn:hover{ background:linear-gradient(180deg,#3f5245,#1e2620); }
.rk-print-btn:active{ transform:scale(.96); }
#rk-print:focus-visible ~ #rk-modal .rk-print-btn{ outline:2px solid #6fbf94; outline-offset:4px; }
@keyframes rk-pulse-ring{
  0%,100%{ box-shadow:0 22px 45px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06), 0 0 0 0 rgba(111,191,148,.45); }
  50%{ box-shadow:0 22px 45px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06), 0 0 0 9px rgba(111,191,148,0); }
}
.rk-print-icon{ font-size:26px; line-height:1; }
.rk-print-text{ color:#EDEAE0 !important; font-size:12px; font-weight:700; letter-spacing:2px; text-transform:uppercase; text-align:center; }
.rk-lamp{
  width:7px; height:7px; border-radius:50%;
  background:#c98a2c; box-shadow:0 0 9px 2px rgba(201,138,44,.75);
  animation:rk-blink 2.4s ease-in-out infinite;
}
@keyframes rk-blink{ 0%,100%{opacity:1;} 50%{opacity:.3;} }

/* fiş yazdırılınca buton küçülüp kaybolur */
#rk-print:checked ~ #rk-modal .rk-print-btn{
  opacity:0; transform:scale(.85); pointer-events:none;
  height:0; padding-top:0; padding-bottom:0; margin-top:-45px; overflow:hidden;
}

/* fiş */
.rk-receipt-wrap{
  width:min(320px,90vw); margin-top:18px;
  opacity:0; transform:translateY(-26px) scaleY(.92); transform-origin:top center;
  pointer-events:none;
  transition:opacity .55s ease, transform .65s cubic-bezier(.2,.8,.2,1), margin .4s ease;
}
#rk-print:checked ~ #rk-modal .rk-receipt-wrap{
  opacity:1; transform:translateY(0) scaleY(1); pointer-events:auto; margin-top:0;
}
.rk-receipt{
  background:#F1EDE0; padding:26px 22px 20px; font-size:12.5px; line-height:1.7;
  box-shadow:0 28px 46px rgba(0,0,0,.5);
}
/* dashboard'ın genel koyu temasını ezip fiş metnini her zaman koyu tutar */
.rk-receipt, .rk-receipt *{ color:#221f19 !important; }
.rk-receipt h3{ margin:0; font-size:15px; letter-spacing:1.5px; text-align:center; }
.rk-sub{ text-align:center; color:#6b675d !important; font-size:10.5px; margin:4px 0; }
.rk-barcode{ height:22px; width:64%; margin:10px auto 3px;
  background:repeating-linear-gradient(90deg,#221f19 0 2px, transparent 2px 4px, #221f19 4px 5px, transparent 5px 9px); }
.rk-barcode-num{ text-align:center; font-size:9px; letter-spacing:3px; color:#8a8576 !important; margin-bottom:6px; }
.rk-dash{ border-top:2px dashed #b9b3a0; margin:11px 0; }
.rk-row{ display:flex; justify-content:space-between; gap:10px; }
.rk-line{ opacity:0; transform:translateY(6px); transition:opacity .35s ease, transform .35s ease; }
#rk-print:checked ~ #rk-modal .rk-line{ opacity:1; transform:translateY(0); }
.rk-l1{transition-delay:.15s;} .rk-l2{transition-delay:.3s;} .rk-l3{transition-delay:.42s;}
.rk-l4{transition-delay:.54s;} .rk-l5{transition-delay:.66s;} .rk-l6{transition-delay:.9s;}
.rk-l7{transition-delay:1.02s;}

.rk-grid{ display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:4px 0 4px; }
.rk-stamp{
  display:block; border:1px solid #b9b3a0; padding:9px; text-align:center;
  text-decoration:none; cursor:pointer; transition:transform .15s ease, border-color .15s ease;
}
.rk-stamp:hover{ border-color:#3f6b4d; transform:translateY(-2px); }
.rk-stamp:active{ transform:translateY(0) scale(.97); }
.rk-stamp img{ width:100%; max-width:78px; height:auto; display:block; margin:0 auto; pointer-events:none; }
.rk-stamp span{ display:block; margin-top:7px; font-size:9.5px; letter-spacing:1.5px; text-transform:uppercase; }
.rk-stamp span::after{ content:" ↗"; }

.rk-total{ display:flex; justify-content:space-between; font-weight:700; margin-top:2px; }
.rk-thanks{ text-align:center; margin-top:8px; font-size:10.5px; color:#3f6b4d !important; }

.rk-tear{
  display:block; text-align:center; margin-top:16px; padding-top:14px;
  border-top:2px dashed #b9b3a0; font-size:12px; letter-spacing:1.5px;
  cursor:pointer; transition:color .2s ease;
}
.rk-tear:hover{ color:#2F6F4E !important; }
#rk-close:focus-visible ~ #rk-modal .rk-tear{ outline:2px solid #6fbf94; outline-offset:4px; }
</style>
<input type="checkbox" id="rk-print">
<input type="checkbox" id="rk-close">
<div id="rk-modal">
<div class="rk-stage">
<label for="rk-print" class="rk-print-btn">
<span class="rk-print-icon">🧾</span>
<span class="rk-print-text">Dokun, Fişini Yazdır</span>
<span class="rk-lamp"></span>
</label>
<div class="rk-receipt-wrap">
<div class="rk-receipt">
<h3 class="rk-line rk-l1">SEPET ANALİZ MARKETİ</h3>
<div class="rk-sub rk-line rk-l1">Fiş No 0007 &middot; FIS_TARIHI_PLACEHOLDER</div>
<div class="rk-barcode rk-line rk-l1"></div>
<div class="rk-barcode-num rk-line rk-l1">E M I N K U C U K 0 0</div>
<div class="rk-dash"></div>
<div class="rk-row rk-line rk-l2"><span>1x HOŞ GELDİN</span><span>ÜCRETSİZ</span></div>
<div class="rk-row rk-line rk-l3"><span>1x SEPET &amp; BİRLİKTELİK ANALİZİ</span><span>DAHİL</span></div>
<div class="rk-dash"></div>
<div class="rk-sub rk-line rk-l4">beni takip et &mdash; indirim yok ama teşekkür var</div>
<div class="rk-grid rk-line rk-l5">
<a class="rk-stamp" href="https://www.linkedin.com/in/eminkucuk00/" target="_blank" rel="noopener"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://www.linkedin.com/in/eminkucuk00/"><span>LinkedIn</span></a>
<a class="rk-stamp" href="https://github.com/Eminkucuk00" target="_blank" rel="noopener"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://github.com/Eminkucuk00"><span>GitHub</span></a>
<a class="rk-stamp" href="https://www.instagram.com/learnwithemin" target="_blank" rel="noopener"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://www.instagram.com/learnwithemin"><span>Instagram</span></a>
<a class="rk-stamp" href="https://medium.com/@eminkucukk00" target="_blank" rel="noopener"><img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://medium.com/@eminkucukk00"><span>Medium</span></a>
</div>
<div class="rk-dash"></div>
<div class="rk-total rk-line rk-l6"><span>TOPLAM</span><span>SINIRSIZ İÇGÖRÜ</span></div>
<div class="rk-thanks rk-line rk-l6">tekrar bekleriz &#10003;</div>
<label for="rk-close" class="rk-tear rk-line rk-l7">&#9986; KESİP DEVAM ET</label>
</div>
</div>
</div>
</div>"""
karsilama_html = karsilama_html.replace("FIS_TARIHI_PLACEHOLDER", date.today().strftime("%d.%m.%Y"))
st.markdown(karsilama_html, unsafe_allow_html=True)

# st.markdown içine gömülen <script> etiketleri tarayıcıda çalışmaz (React innerHTML kısıtlaması),
# bu yüzden fişi kesince sidebar'ı açan JS'i gerçekten çalışan bir iframe (components.html) ile çalıştırıyoruz.
components.html(
    """
    <script>
    setInterval(function(){
      try{
        var kesCheckbox = window.parent.document.getElementById('rk-close');
        if(kesCheckbox && kesCheckbox.checked){
          window.parent.document.body.classList.add('rk-unlocked');
        }
      }catch(e){}
    }, 250);
    </script>
    """,
    height=0,
    width=0,
)

# 3. Veri Yükleme
ana_veri, siparisler = veri_yukle()

# Lottie animasyonu fonksiyonu
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 4. Sol Menü (Sidebar) - Dinamik Filtreleme
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'><span class='material-symbols-rounded'>tune</span> Filtreler</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    secilen_gun = st.radio(
        ":material/calendar_month: Gün Seçimi:",
        ["Tümü", "Hafta İçi", "Hafta Sonu"]
    )
    
    secilen_saat = st.radio(
        ":material/schedule: Saat Aralığı:",
        ["Tümü", "Sabah (06-12)", "Öğle (12-18)", "Akşam (18-24)"]
    )
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.info("Bu filtreler tüm dashboard'daki analizleri dinamik olarak etkiler.")

# Filtreleri Uygula
filtrelenmis_veri = veriyi_filtrele(ana_veri, secilen_gun, secilen_saat)
kpis = kpi_hesapla(filtrelenmis_veri)

# 5. Üst Navigasyon (Yatay Menü) - Floating Island Tasarımı
secili_sekme = option_menu(
    menu_title=None,
    options=["Genel Bakış", "Ağ Analizi", "Cross-Sell AI"],
    icons=["bar-chart-line", "diagram-3", "robot"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "5px!important", 
            "background": "rgba(10, 10, 25, 0.5)", 
            "border": "1px solid rgba(255, 255, 255, 0.1)", 
            "border-radius": "50px",
            "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
            "backdrop-filter": "blur(20px)",
            "width": "80%",
            "margin": "0 auto"
        },
        "icon": {"color": "#06b6d4", "font-size": "18px"}, 
        "nav-link": {
            "font-size": "15px", 
            "text-align": "center", 
            "margin":"0px", 
            "--hover-color": "rgba(255,255,255,0.05)", 
            "color": "white",
            "border-radius": "50px",
            "transition": "all 0.3s ease"
        },
        "nav-link-selected": {
            "background": "linear-gradient(90deg, #8b5cf6, #ec4899)",
            "border-radius": "50px",
            "box-shadow": "0 4px 15px rgba(236, 72, 153, 0.4)",
            "font-weight": "bold"
        },
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Sekmelerin İçerikleri
if secili_sekme == "Genel Bakış":
    # 4'lü KPI Kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h4><span class="material-symbols-rounded">receipt_long</span> Toplam Fiş</h4>
            <h2>{kpis['toplam_fis']['deger']}</h2>
            <p style="color:#22c55e; font-size:12px;">{kpis['toplam_fis']['delta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <h4><span class="material-symbols-rounded">shopping_cart</span> Ort. Sepet</h4>
            <h2>{kpis['ort_sepet']['deger']}</h2>
            <p style="color:#ef4444; font-size:12px;">{kpis['ort_sepet']['delta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <h4><span class="material-symbols-rounded">inventory_2</span> Ürün Çeşidi</h4>
            <h2>{kpis['urun_cesidi']['deger']}</h2>
            <p style="color:#22c55e; font-size:12px;">{kpis['urun_cesidi']['delta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <h4><span class="material-symbols-rounded">favorite</span> Sadakat Oranı</h4>
            <h2>{kpis['sadakat_orani']['deger']}</h2>
            <p style="color:#22c55e; font-size:12px;">{kpis['sadakat_orani']['delta']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Yan Yana 2 Grafik
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.plotly_chart(ciz_en_cok_satanlar(filtrelenmis_veri), use_container_width=True, theme=None)
        
    with col_g2:
        st.plotly_chart(ciz_gercek_sadakat(filtrelenmis_veri), use_container_width=True, theme=None)
        
    # Heatmap
    st.plotly_chart(ciz_heatmap(filtrelenmis_veri), use_container_width=True, theme=None)

elif secili_sekme == "Ağ Analizi":
    st.markdown("### :material/hub: Ürün Birliktelik Ağı (Association Rules)")
    
    with st.spinner("Apriori Algoritması çalışıyor, kurallar hesaplanıyor... (Bu işlem birkaç saniye sürebilir)"):
        kurallar = association_rules_hesapla(filtrelenmis_veri)
        
    if kurallar.empty:
        st.warning("Bu filtre kombinasyonu için anlamlı kural bulunamadı. Lütfen filtreleri gevşetin.")
    else:
        col_n1, col_n2 = st.columns([1, 1])
        
        with col_n1:
            st.plotly_chart(ciz_network_graph(kurallar), use_container_width=True, theme=None)
            
        with col_n2:
            st.plotly_chart(ciz_sepet_buyuklugu(filtrelenmis_veri), use_container_width=True, theme=None)
            
        st.markdown("#### :material/list_alt: Algoritma Sonuçları (Sıralanabilir Tablo)")
        gosterim_tablosu = kurallar[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values(by='lift', ascending=False)
        st.dataframe(gosterim_tablosu.head(20), use_container_width=True)

elif secili_sekme == "Cross-Sell AI":
    st.markdown("### :material/track_changes: AI Destekli Çapraz Satış (Cross-Sell) Motoru")
    st.write("Müşterinin sepetine eklediği ürünü seçin, öneri motorumuz en yüksek sinerjiye sahip ürünleri getirsin.")
    
    kurallar = association_rules_hesapla(filtrelenmis_veri)
    
    if kurallar.empty:
        st.warning("Bu filtreler için kural üretilemedi.")
    else:
        tekil_urunler = list(set(kurallar['antecedents'].unique()))
        
        # Lottie Loading (Süsleme)
        lottie_search = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_t24tudjw.json")
        
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            secilen_urun = st.selectbox(":material/search: Ürün Ara ve Seç:", sorted(tekil_urunler))
            if lottie_search:
                from streamlit_lottie import st_lottie
                st_lottie(lottie_search, height=150, key="search_anim")
                
        with col_s2:
            oneriler = kurallar[kurallar['antecedents'] == secilen_urun].sort_values(by=['lift', 'confidence'], ascending=[False, False])
            
            if oneriler.empty:
                st.info(f"'{secilen_urun}' için yeterince güçlü bir tamamlayıcı ürün bulunamadı.")
            else:
                st.markdown(f'<h4><span class="material-symbols-rounded">lightbulb</span> "{secilen_urun}" Alan Müşteriye Öneriler</h4>', unsafe_allow_html=True)
                
                gosterilecek = oneriler[['consequents', 'support', 'confidence', 'lift']].head(5)
                st.dataframe(gosterilecek, use_container_width=True)
                
                # CSV Export
                csv = gosterilecek.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Pazarlama Ekibi İçin İndir (CSV)",
                    icon=":material/download:",
                    data=csv,
                    file_name=f"{secilen_urun}_onerileri.csv",
                    mime="text/csv",
                    type="primary"
                )
