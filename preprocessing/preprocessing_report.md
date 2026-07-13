# Preprocessing Adımları Dokümantasyonu
## Sprint 5 — Feature Engineering & Preprocessing
**Proje**: Kredi Kartı Müşteri Kaybı (Churn) Analizi  
**Dataset**: BankChurners.csv (10,127 satır × 23 kolon)  
**Hazırlayan**: Mehmet Emin Küçük

---

## 1. Silinen Kolonlar ve Gerekçeleri

### Data Leakage Riski
| Kolon | Gerekçe |
|---|---|
| Naive_Bayes_..._1 | Önceden eğitilmiş bir modelin olasılık çıktısı. Modele verilirse haksız %100 doğruluk verir. |
| Naive_Bayes_..._2 | Aynı data leakage riski. |

### Multicollinearity
| Kolon | Gerekçe |
|---|---|
| Avg_Open_To_Buy | Credit_Limit - Total_Revolving_Bal formülüyle hesaplanır. Credit_Limit ile korelasyonu ~0.99. |

### İstatistiksel Olarak Anlamsız (Kalan vs Giden Farkı Düşük)
| Kolon | Fark % | p-value | Gerekçe |
|---|---|---|---|
| Customer_Age | %0.9 | 0.067 | Yaş dağılımı giden ve kalanlarda neredeyse aynı |
| Months_on_book | %0.8 | 0.168 | Kıdem farkı yok |
| Dependent_count | %2.9 | 0.056 | Aile büyüklüğü churn'ü etkilemiyor |
| Gender | Cramers V=0.037 | 0.0002 | Etki büyüklüğü çok küçük |
| Marital_Status | Cramers V=0.025 | 0.109 | İstatistiksel olarak anlamlı değil |
| Income_Category | Cramers V=0.036 | 0.025 | Tüm gelir gruplarında churn oranı birbirine yakın |

### Tutulan Kategorik Değişkenler
| Kolon | Tutulma Gerekçesi |
|---|---|
| Card_Category | Platinum segmentinde %25 churn (genel %16.1) — güçlü sinyal |
| Education_Level | Doktora mezunlarında %21.1 churn — anlamlı fark |

---

## 2. Feature Engineering (Türetilen Yeni Değişkenler)

| Yeni Feature | Formül | Açıklama |
|---|---|---|
| Avg_Trans_Value | Total_Trans_Amt / Total_Trans_Ct | Ortalama işlem büyüklüğü |
| Activity_Rate | (12 - Months_Inactive_12_mon) / 12 | Aktiflik oranı (1.0 = her ay aktif) |
| Revolving_to_Limit | Total_Revolving_Bal / Credit_Limit | Limitin ne kadarı faize bırakılıyor |
| Limit_per_Trans | Credit_Limit / Total_Trans_Ct | Her işleme düşen limit |
| Change_Score | Total_Amt_Chng_Q4_Q1 x Total_Ct_Chng_Q4_Q1 | Harcama ve işlem değişimini birleştiren skor |

---

## 3. Encoding Yöntemleri

| Kolon | Yöntem | Dönüşüm |
|---|---|---|
| Attrition_Flag | Binary | Existing Customer=0, Attrited Customer=1 |
| Education_Level | Ordinal | Uneducated=0, High School=1, College=2, Graduate=3, Post-Graduate=4, Doctorate=5, Unknown=3 |
| Card_Category | Ordinal | Blue=0, Silver=1, Gold=2, Platinum=3 |

---

## 4. Eksik Değer Yaklaşımı

NaN/NULL eksik değer bulunmamaktadır. Unknown değerleri ayrı bir kategori olarak korunmuş, encoding sırasında orta değere atanmıştır.

| Kolon | Unknown Adedi | Oran |
|---|---|---|
| Education_Level | 1,519 | %15.0 |

---

## 5. Scaling

- Yöntem: StandardScaler (ortalama=0, std=1)
- Train'den öğrenildi (fit_transform), test'e uygulandı (transform) — leakage önleme

---

## 6. Train/Test Split

| Parametre | Değer |
|---|---|
| Test oranı | %20 |
| Stratified | Evet |
| Random state | 42 |
| Train | 8,101 x 17 |
| Test | 2,026 x 17 |

---

## 7. Çıktı Dosyaları

| Dosya | Boyut |
|---|---|
| X_train.csv | 8,101 x 17 |
| X_test.csv | 2,026 x 17 |
| y_train.csv | 8,101 x 1 |
| y_test.csv | 2,026 x 1 |
