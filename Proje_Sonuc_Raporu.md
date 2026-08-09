# Banka Müşteri Terk (Churn) Tahmini - Proje Dokümantasyonu

Geliştirdiğim Kredi Kartı Müşteri Terk (Churn) Tahmini projesinin amaçlarını, süreçlerini ve elde ettiğim sonuçları (Acceptance Criteria maddelerine birebir uygun olarak) bu dokümanda detaylandırdım.

---

## 1. Problem Tanımı ve Kullanılan Veri Seti

### Problem Tanımı
Bankacılık sektöründe yeni bir müşteri kazanmanın, mevcut müşteriyi elde tutmaktan çok daha maliyetli olduğunu gözlemledim. Bu doğrultuda; kredi kartı müşterilerinin kurumu terk etme (churn) eğilimlerini önceden tespit edebilen bir yapay zeka modeli geliştirmeyi ve şube müdürlerinin proaktif aksiyon almasını sağlayacak bir risk tablosu oluşturmayı amaçladım.

### Veri Seti
Projemi geliştirirken Kaggle platformunda bulunan **Credit Card Customers (BankChurners.csv)** veri setini kullandım.
- **Boyut:** Veri setinde toplam 10.127 müşteri kaydı bulunuyordu.
- **Dengesizlik:** Müşterilerin yaklaşık %16'sının kurumu terk ettiğini (Attrited Customer), %84'ünün ise mevcut müşteri (Existing Customer) olduğunu analiz ettim.
- **Özellikler:** Müşterilere ait yaş, eğitim, gelir gibi demografik bilgiler ile kredi limiti, işlem adedi ve işlem hacmi gibi finansal davranış verilerini inceledim.

---

## 2. Modelleme Süreci ve Veri Hazırlama

Modelimin en doğru şekilde öğrenebilmesi için baştan uca bir "Veri Temizleme Fabrikası" (Pipeline) kodladım. Bu süreçte şu adımları uyguladım:

1. **Özellik Mühendisliği (Feature Engineering):** Modelin müşteri davranışını daha iyi kavraması için ham verilerden 5 yeni matematiksel değişken ürettim:
   - `Avg_Trans_Value`: İşlem başına ortalama harcama tutarını hesapladım.
   - `Activity_Rate`: Müşterinin 12 aylık periyottaki aktiflik oranını çıkardım.
   - `Revolving_to_limit`: Kredi limiti kullanım ve borçluluk oranını buldum.
   - `Limit_per_Trans`: İşlem başına kalan kredi limitini hesapladım.
   - `Change_Score`: İşlem hacmi ve işlem adedindeki çeyreklik değişim ivmesini modelledim.
2. **Gereksiz Kolonların Temizlenmesi:** Yaptığım analizler sonucunda churn ile istatistiksel bağı olmayan (Yaş, Cinsiyet, Medeni Hal vb.) özellikleri ve modelin kopya çekmesine (Data Leakage) sebep olabilecek veri sızıntısı kolonlarını tablodan sildim.
3. **One-Hot Encoding:** Kategorik metin verilerini makinenin anlayabileceği 0-1 formatına dönüştürdüm. Aldığım kural kararı doğrultusunda "Unknown" (Bilinmeyen) değerleri medyan ile doldurmak yerine, modelin bağımsız bir müşteri psikolojisi olarak öğrenmesi için kasıtlı olarak `-1` değeriyle değiştirdim.
4. **Veri Dengesizliğinin Çözümü (SMOTE):** Veri setindeki %16'lık churn sınıfının modelin öğrenmesini zorlaştırdığını fark ettim. Bu sorunu çözmek için sadece eğitim (Train) veri setine SMOTE (Sentetik Azınlık Aşırı Örnekleme Tekniği) uygulayarak, azınlık sınıfı klonladım ve veriyi %50-%50 oranında dengeledim. (Test veri setine kesinlikle dokunmadım).

---

## 3. Denenen Modeller ve Final Model Seçimi Gerekçesi

Modelleme aşamasında Logistic Regression, Random Forest, LightGBM ve XGBoost algoritmalarını test ettim. 

### Neden XGBoost'u Seçtim?
- Yüksek boyutlu finansal verilerdeki karmaşık ilişkileri en doğru yakalayan modelin **XGBoost Classifier** olduğunu tespit ettim.
- Overfitting (ezberleme) probleminin önüne geçmek için karar ağaçlarının derinliğini (`max_depth=6`) ve öğrenme hızını (`learning_rate=0.1`) optimize ettim. Yaptığım Çapraz Doğrulama (Cross-Validation) testlerinde en istikrarlı performansı bu modelden aldım.

### Eşik Değeri (Threshold) Gerekçesi: Neden 0.30?
Standart yapay zeka modellerinde eşik değeri genellikle 0.50 olarak kabul edilir. Ancak bankacılık mantığında bir müşteriyi **kaçırmanın (False Negative) maliyetinin**, kalacak bir müşteriyi gereksiz yere **aramaktan (False Positive) çok daha yüksek olduğunu** analiz ettim.
Yaptığım finansal simülasyonlarda (Robustness Checks) eşik değerini 0.30'a çektiğimde:
- Gidecek müşterileri önceden yakalama oranımı (Recall) maksimize ettim.
- Artan gereksiz çağrı merkezi maliyetlerinin, kurtarılan müşterilerin getireceği kazancın yanında ihmal edilebilir kaldığını kanıtladım. Böylece banka için en kârlı "Sweet Spot" (Tatlı Nokta) değerinin **0.30** olduğunu matematiksel olarak ispatlayarak bu eşiği final modelime entegre ettim.

---

## 4. Risk Segmentasyonu ve Aksiyon Yaklaşımı

Hesapladığım 0.00 ile 1.00 arasındaki Churn olasılıklarını, iş birimlerinin kolayca stratejik karar alabilmesi için 0.30 kâr eşiğimi baz alarak 3 ana segmente böldüm:

| Segment | Churn İhtimali | Şubeye Önerdiğim Aksiyon |
|---------|----------------|--------------------------|
| 🟢 **Düşük Risk** | 0.00 - 0.30 | Aksiyon Gerekmez |
| 🟡 **Orta Risk** | 0.30 - 0.60 | Hedefli Pazarlama / Çarpraz Satış Kampanyası |
| 🔴 **Yüksek Risk** | 0.60 - 1.00 | Acil Arama ve Özel İkna Teklifi Sunulması |

---

## 5. Çıktı Tablosu Kolonları (Output)

Projemin nihai ürünü olarak Şube Müdürlerinin kullanması için `Musteri_Risk_Cikti_Tablosu_Guncel.csv` adında eyleme geçirilebilir bir liste ürettim. Bu tablodaki kolonları şu şekilde tasarladım:

- `Musteri_ID`: Şube personelinin müşteriye ulaşabilmesi için bankadaki benzersiz hesap numarası.
- `Churn_Probability`: Modelimin hesapladığı, müşterinin bankayı terk etme olasılığı (Örn: 0.812).
- `Gercek Durum`: Müşterinin reel durumu (Bu kolonu model test ve simülasyonlarımı yapabilmek için ekledim).
- `Risk_Segmenti`: Yukarıda belirlediğim eşiklere göre müşterinin düştüğü kategori (Yüksek, Orta, Düşük Risk).
- `Onerilen_Aksiyon`: Şube temsilcisine yönlendirdiğim iş direktifi.
- `Ana_Risk_Nedeni`: SHAP Yapay Zeka dedektifini kullanarak, her müşteri için özel olarak hesaplattığım **"kişiyi bankadan ayrılmaya iten en büyük tetikleyici faktör"**. (Örn: "Total_Trans_Ct" azalması). Bu sayede personelin müşteriyi doğru argümanla aramasını sağladım.

---

## 6. Limitasyonlar ve Sonraki Adımlar (Next Steps)

Projemin sonunda sistemin geliştirilmeye açık yönlerini (Limitasyonlar) ve bir sonraki aşamada yapılabilecekleri (Next Steps) şu şekilde özetledim:

### Karşılaştığım Limitasyonlar
1. **Zaman Serisi Eksikliği:** Kullandığım Kaggle veri setinin anlık bir kesiti (snapshot) yansıtması nedeniyle, müşterilerin aylar içindeki harcama düşüş trendlerini dinamik bir zaman serisi olarak inceleme imkanım olmadı.
2. **Canlı Entegrasyon:** Geliştirdiğim sistem şu an için statik CSV dosyaları üzerinden çalışıyor. Gerçek bir banka ortamındaki gibi canlı bir veritabanına bağlı bulunmuyor.

### Önerdiğim Sonraki Adımlar (Next Steps)
1. **Veritabanı Entegrasyonu:** Modelin CSV yerine PostgreSQL veya AWS S3 gibi kaynaklar üzerinden canlı veri akışına (Data Pipeline) entegre edilmesini ve günlük olarak otomatik çalıştırılmasını planlayabiliriz.
2. **Zaman Serisi Modelleri:** LSTM (Long Short-Term Memory) gibi derin öğrenme destekli zaman serisi modelleri kurarak, müşteri davranışlarındaki tarihsel ivmeyi daha güçlü yakalayabiliriz.
3. **Otomatik CRM Bildirimleri:** Belirlediğim 0.30 kâr eşiğini aşan yüksek riskli bir müşteri tespit edildiğinde, bankanın Müşteri İlişkileri (CRM) sistemine otomatik "Uyarı / Arama Kartı" düşüren veya doğrudan müşteriye SMS tetikleyen bir API entegrasyonu yazabiliriz.
