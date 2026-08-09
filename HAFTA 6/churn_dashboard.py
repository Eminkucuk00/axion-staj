import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(
    page_title="Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def veri_yukle():
    dosya_yolu =dosya_yolu = "Musteri_Risk_Cikti_Tablosu_Guncel.csv"
    df = pd.read_csv(dosya_yolu)
    return df

df = veri_yukle()

RENK_HARITASI = {
    "Yüksek Risk" : "#FF4D4D",
    "Orta Risk": "#FFA500",
    "Düşük Risk" : "#00C97B"
}

st.sidebar.title("🎛️ Filtreler")

tum_segmentler = df["Risk_Segmenti"].unique().tolist()

secili_segmentler = st.sidebar.multiselect(
    label = "Risk Segmenti Seçin:",
    options = tum_segmentler,
    default = tum_segmentler
)

min_olas, max_olas = st.sidebar.slider(
    label = "Churn Olasılık Aralığı :",
    min_value=0.0,
    max_value=1.0,
    value=(0.0,1.0),
    step=0.01
)

filtreli_df = df[
    (df["Risk_Segmenti"].isin(secili_segmentler)) &
    (df["Churn_Probability"] >= min_olas) &
    (df["Churn_Probability"] <= max_olas)

].copy()

st.sidebar.markdown("---")
st.sidebar.metric(
    label="Filtrelenen Müşteri Sayısı",
    value=f"{len(filtreli_df):,}"
)

st.title("📊 Churn Dashboard - Müşteri Kayıp Riski Panosu")
st.markdown("*XGBoost (SMOTE + 0.30) modeli çıktıları üzerinden interaktif analiz*")
st.markdown("---")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        label="👥 Toplam Müşteri", 
        value=f"{len(filtreli_df):,}"
    )

with kpi2:
    yuksek_risk_sayisi = len(filtreli_df[filtreli_df["Risk_Segmenti"] == "Yüksek Risk"])
    st.metric(
        label="🔴 Yüksek Riskli", 
        value=f"{yuksek_risk_sayisi:,}"
    )    

with kpi3:

    ortalama_olasilik = filtreli_df["Churn_Probability"].mean()
    st.metric(
        label="📈 Ort. Churn Olasılığı", 
        value=f"%{ortalama_olasilik * 100:.1f}"
    )

with kpi4:
    risk_altindaki_ciro = filtreli_df.loc[filtreli_df["Risk_Segmenti"] == "Yüksek Risk", "Total_Trans_Amt"].sum()
    st.metric(label="💸 Risk altındaki Ciro", value=f"${risk_altindaki_ciro:,.0f}")

with kpi5:
    st.metric(label="🎯 Model Recall",
    value="%90.5"
    )

st.markdown("---")      

grafik_sol, grafik_sag = st.columns(2)

with grafik_sol:
    st.subheader("🥧 Risk Segment Dağılımı")

    segment_sayilari = filtreli_df["Risk_Segmenti"].value_counts().reset_index()
    segment_sayilari.columns = ["Risk_Segmenti", "Musteri_Sayisi"]

    fig_pasta = px.pie(
        data_frame=segment_sayilari,             # Çizilecek veri tablosu
        names="Risk_Segmenti",                   # Dilimlerin isimleri
        values="Musteri_Sayisi",                 # Dilimlerin büyüklüğü
        color="Risk_Segmenti",                   # Dilimleri segment ismine göre renklendir
        color_discrete_map=RENK_HARITASI,        # Adım 2'de tanımladığımız özel renk sözlüğü
        hole=0.4                                 # Ortasında %40'lık bir delik aç (Donut yapar)
    )

    fig_pasta.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",           # Dış arkaplanı şeffaf yap
        plot_bgcolor="rgba(0,0,0,0)",            # İç arkaplanı şeffaf yap
        height=400                               # Grafiğin boyu (piksel)
    )

    fig_pasta.update_traces(textinfo="label+percent+value", textfont_size=12)

    st.plotly_chart(fig_pasta, use_container_width=True)

with grafik_sag:
    st.subheader("📊 Churn Olasılık Dağılımı")

    fig_hist = px.histogram(
        data_frame=filtreli_df,                  # Veri kaynağımız
        x="Churn_Probability",                   # X ekseninde 0 ile 1 arasındaki olasılıklar olsun
        color="Risk_Segmenti",                   # Çubukları risk segmentine göre renklendir
        color_discrete_map=RENK_HARITASI,        # Yine bizim özel renk sözlüğümüz (Yeşil, Turuncu, Kırmızı)
        nbins=50,                                # Veriyi 50 adet ince çubuğa (bin) böl
        labels={"Churn_Probability": "Churn Olasılığı", "count": "Müşteri Sayısı"},
        barmode="overlay"                        # Çubuklar yan yana değil, birbiri üstüne binsin (şeffaf şekilde)
    )

    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),  # Arkadaki ızgara (grid) çizgilerini hafif beyaz yap
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
    )

    fig_hist.update_traces(opacity=0.7)

    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

st.subheader("⚠️ En Önemli Risk Faktörleri - Müşterileri Kaçıran Değişkenler")

risk_faktor_sayilari = (
    filtreli_df["Ana_Risk_Nedeni"]
    .value_counts()
    .reset_index()
)
risk_faktor_sayilari.columns = ["Risk_Faktoru", "Musteri_Sayisi"]


fig_bar = px.bar(
    data_frame=risk_faktor_sayilari,
    x="Musteri_Sayisi",
    y="Risk_Faktoru",
    orientation="h",
    color="Musteri_Sayisi",
    color_continuous_scale=["#00C97B", "#FFA500", "#FF4D4D"],

    labels={
        "Musteri_Sayisi": "Etkilenen Müşteri Sayısı",
        "Risk_Faktoru":  "Risk Faktörü"
    }
)

fig_bar.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=400,
    showlegend=False,
    xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.1)",
        categoryorder="total ascending"
    )
)

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")


st.subheader("🔴 Yüksek Riskli Müşteri Listesi (Aksiyon Tablosu)")

gosterilecek_kolonlar = [
    "Musteri_ID",
    "Churn_Probability",
    "Risk_Segmenti",
    "Onerilen_Aksiyon",
    "Ana_Risk_Nedeni",
    "Months_on_book",
    "Credit_Limit",
    "Total_Trans_Ct",
    "Total_Trans_Amt",
    "Total_Revolving_Bal",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Total_Relationship_Count"

]

gosterilecek_sayi = st.slider(
    label="Ekranda Kaç Müşteri Listelensin?",
    min_value=5,
    max_value=min(100, len(filtreli_df)),
    value=20,
    step=5
)

tablo_df = (
    filtreli_df[gosterilecek_kolonlar]
    .sort_values("Churn_Probability", ascending=False)
    .head(gosterilecek_sayi)
    .reset_index(drop=True)
)

tablo_df.columns = [
    "Müşteri ID",
    "Olasılık (%)",
    "Risk Segmenti",
    "Önerilen Aksiyon",
    "Ana Neden",
    "Kıdem (Ay)",
    "Kredi Limiti",
    "İşlem Sayısı",
    "Toplam Hacim",
    "Borç Bakiyesi",
    "Hareketsiz Ay",
    "İletişim Sayısı",
    "Ürün Sayısı"
]

tablo_df["Olasılık (%)"] = tablo_df["Olasılık (%)"].apply(lambda x: f"%{x*100:.1f}")

st.dataframe(
    data=tablo_df,
    use_container_width=True,
    height=500
)

st.markdown("---")

st.caption("📌 Model: XGBoost (SMOTE + Eşik 0.30)  | Veri: 2026 Test Müşterisi | Hazırlayan: Mehmet Emin KÜÇÜK")
