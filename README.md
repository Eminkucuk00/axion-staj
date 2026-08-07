# Bank Customer Churn Prediction & Dashboard

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-emin--churn.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://emin-churn.streamlit.app/)

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
- **Çıktı:** 10.127 müşterinin tamamını 0.30 optimum eşik mantığıyla skorlar ve `Musteri_Risk_Cikti_Tablosu_Guncel.csv` tablosunu üretir.

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
