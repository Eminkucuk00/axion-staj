# Bank Customer Churn Prediction & Dashboard

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

## Nasıl Kullanılır?

1. Kodu çalıştırarak modeli eğitin ve güncel risk tablosunu oluşturun:
   ```bash
   python "HAFTA 6/final_pipeline.py"
   ```
2. Paneli (Dashboard) başlatarak analizleri görüntüleyin:
   ```bash
   streamlit run "HAFTA 6/churn_dashboard.py"
   ```
