# AXION Data Analytics Internship — Churn Prediction & Market Basket Analysis

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-emin--churn.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://emin-churn.streamlit.app/)

Bu repo, AXION'daki 8 haftalık Data Analytics stajında geliştirilen iki uçtan uca veri bilimi projesini içerir:

| Proje | Klasör | Özet |
|---|---|---|
| **1. Banka Müşteri Churn Tahmini & Dashboard** | `HAFTA 6/` | XGBoost + SMOTE + SHAP ile churn tahmini (recall %92,6), müşteri risk tablosu ve canlı Streamlit paneli |
| **2. Market Basket Analysis & Cross-Sell Dashboard** | `HAFTA 8/` | Instacart verisinde FP-Growth ile birliktelik kuralları (lift 4,23'e kadar), cross-sell öneri motoru ve üç sekmeli Streamlit paneli |

---

# Proje 1 — Bank Customer Churn Prediction & Dashboard

Bu proje, banka müşterilerinin kurumu terk etme (churn) riskini makine öğrenmesi teknikleriyle tahmin etmeyi ve sonuçları interaktif bir arayüzle sunmayı amaçlamaktadır.

## Proje İçeriği

Bu repository sadece en iyi sonuç veren, üretim ortamına (production) hazır, uçtan uca çalışan profesyonel kodları içermektedir:

### 1. `HAFTA 6/final_pipeline.py`
Bu dosya, ham veri setini alan ve makine öğrenmesi modelini uçtan uca eğiten **Kusursuz Veri Ön İşleme ve Modelleme** scriptidir.
- **Özellik Mühendisliği (Feature Engineering):** Ham veriden iş zekasına uygun 5 yeni matematiksel değişken üretir.
- **Veri Temizliği:** Modelde kopya çekilmesine (data leakage) yol açabilecek veya gereksiz olan kolonları temizler.
- **Dengesiz Veri Çözümü (SMOTE):** Churn (terk eden) müşteri sayısının azlığını SMOTE algoritmasıyla dengeler.
- **Model Eğitimi:** XGBoost algoritmasını `max_depth=6`, `learning_rate=0.1` hiperparametreleriyle eğitir.
- **Açıklanabilirlik (SHAP):** Sadece kimin churn olacağını tahmin etmekle kalmaz, **SHAP TreeExplainer** kullanarak her müşterinin *neden* riskli olduğunu (Ana Risk Nedeni) matematiksel olarak kanıtlar.
- **Çıktı:** 10.127 müşterinin tamamını 0.40 eşik değeriyle skorlar ve `Musteri_Risk_Cikti_Tablosu_Guncel.csv` tablosunu üretir.

### 2. `HAFTA 6/churn_dashboard.py`
Bu dosya, eğitilen modelin ürettiği sonuçları (CSV tablosunu) iş birimlerinin (yöneticilerin, şube müdürlerinin) kullanımına sunan **Streamlit** tabanlı interaktif bir web arayüzüdür.
- Dinamik filtreleme ile Yüksek, Orta, Düşük riskli müşterilerin anlık analizi.
- Müşterileri kaybetmemize yol açan en önemli "Risk Faktörleri"nin grafiksel sunumu.
- Hangi müşteriye hangi aksiyonun alınması gerektiğini gösteren (Örn: Acil Arama ve İkna Teklifi) listeler.

### 3. `HAFTA 6/robustness_checks.py` ve `Model_Validation_and_Robustness_Report.md`
Bu dosyalar, modelin dayanıklılığını (robustness) matematiksel olarak kanıtlayan test scripti ve bu testin sonuçlarına dayalı detaylı **İş Mantığı ve Güvenilirlik Raporu**'dur.
- **Overfitting Kontrolü:** Modelin train/test performansını (Accuracy, Recall) kıyaslayarak aşırı öğrenme yapmadığını doğrular.
- **Cross-Validation:** 5-Fold CV ile modelin başarı şansının tesadüf olmadığını, son derece istikrarlı olduğunu kanıtlar.
- **SMOTE Etkisi:** Dengeli ve dengesiz verileri kıyaslayarak SMOTE'un "Gidecek Müşteriyi Yakalama (Recall)" oranını artırarak iş birimine nasıl güven verdiğini gösterir.
- **Threshold Analizi (Confusion Matrix):** Karar eşik değeri 0.30'a çekildiğinde fazladan oluşacak çağrı maliyetlerinin (FP), bankayı terk edecek fazladan müşterilerin (FN) yaratacağı finansal zarardan çok daha küçük olduğunu kanıtlar ve projenin optimum noktasının (sweet spot) **0.30** olduğunu bilimsel olarak ispatlar.

## Nasıl Kullanılır?

1. Kodu çalıştırarak modeli eğitin ve güncel risk tablosunu oluşturun:
   ```bash
   python "HAFTA 6/final_pipeline.py"
   ```
2. Paneli (Dashboard) başlatarak analizleri görüntüleyin:
   ```bash
   streamlit run "HAFTA 6/churn_dashboard.py"
   ```

---

# Proje 2 — Market Basket Analysis & Cross-Sell Dashboard (`HAFTA 8/`)

Instacart açık veri seti (33,7 milyon sipariş-ürün satırı) üzerinde müşterilerin sepet alışkanlıklarını analiz eden, ürün birliktelik kurallarını çıkaran ve bu kurallardan çapraz satış (cross-sell) önerileri üreten projedir.

### 1. `HAFTA 8/instacart_analysis.ipynb`
Uçtan uca analiz notebook'u:
- **Veri temizleme:** `orders`, `order_products`, `products`, `aisles`, `departments` tablolarının birleştirilmesi; eksik/duplicate kontrolü; bellek için `category` dtype ve `usecols` kullanımı.
- **Sepet EDA'sı:** toplam sipariş / ürün / müşteri sayıları, sepet başına ortalama ürün, en çok satan ürünler, gün-saat yoğunluk haritası, **genel reorder oranı %59,9**.
- **Association rules (FP-Growth, `mlxtend`):** 130.044 sipariş ve en çok satan 10.000 ürün üzerinde sparse sepet matrisi; `min_support = 0,01`, `lift ≥ 1,2` filtresi.
- **Öne çıkan kurallar:** Limes → Large Lemon (**lift 4,23**), Organic Hass Avocado → Bag of Organic Bananas (**confidence %33,2**).
- **Cross-sell öneri fonksiyonu:** seçilen ürün için kuralları lift ve confidence'a göre sıralayıp tamamlayıcı ürünleri listeler.

### 2. `HAFTA 8/dashboard.py` + `HAFTA 8/utils/`
Üç sekmeli, modüler **Streamlit** paneli (`streamlit-option-menu`):
- **Genel Bakış:** sepet KPI'ları, en çok satanlar, gerçek sadakat (reorder) grafiği, sepet büyüklüğü dağılımı, gün-saat heatmap'i.
- **Ağ Analizi:** birliktelik kurallarının `networkx` + Plotly ile ürün ağı olarak görselleştirilmesi.
- **Cross-Sell AI:** ürün seçildiğinde lift/confidence'a göre önceliklendirilmiş tamamlayıcı ürün önerileri; gün ve saat filtresine göre kuralların yeniden hesaplanması.

Yardımcı modüller: `veri_islemleri.py` (yükleme, filtreleme, kural hesaplama), `kpi_hesaplayici.py`, `gorsellestirme.py`, `css_motoru.py`.

### Nasıl Çalıştırılır?
```bash
cd "HAFTA 8"
pip install -r ../requirements.txt
streamlit run dashboard.py
```
`HAFTA 8/data/` altındaki `.zip` dosyaları ilk çalıştırmada otomatik okunur; ham `.csv` dosyaları boyutları nedeniyle repoya dahil edilmemiştir (`.gitignore`).
