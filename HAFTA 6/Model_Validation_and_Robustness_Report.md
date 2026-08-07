# Model Validation & Robustness Checks 

Bu rapor, Banka Müşteri Kaybı (Churn) Tahmin Modeli'nin dayanıklılığını, güvenilirliğini ve sınırlarını test etmek amacıyla oluşturulmuştur. Tüm değerlendirmeler, model üzerinde yapılan ampirik (gerçek veriye dayalı) testlerin sonuçlarına göre hazırlanmıştır.

---

### 1. Train/Test Performans Farkı ve Overfitting (Aşırı Öğrenme) Kontrolü

Modelin eğitim (train) ve test (test) setlerindeki performansı karşılaştırıldığında şu sonuçlar elde edilmiştir:
- **Train Seti:** Accuracy: 0.9939 | Recall: 0.9968 | Log Loss: 0.0307
- **Test Seti:** Accuracy: 0.9580 | Recall: 0.9015 | Log Loss: 0.0979
*(Not: Bu ilk kontrol aşamasındaki metrikler, projenin başlangıcında hedeflenen 0.40 eşik değerine göre hesaplanmıştır.)*

**Yorum:** XGBoost gibi ağaç tabanlı güçlü algoritmaların doğası gereği eğitim setinde (train) metriklerin %99 seviyelerine çıkması normaldir. Önemli olan modelin daha önce **hiç görmediği** test verisindeki başarısıdır. Test setinde Recall (kaybedilecek müşteriyi yakalama) değerinin %90.15 ve genel doğruluğun %95.80 gibi son derece yüksek seviyelerde kalması, modelin veriyi "ezberlemediğini" (overfitting yapmadığını), aksine altta yatan örüntüleri (patterns) başarıyla "öğrenip genellediğini" kanıtlamaktadır. 

---

### 2. Cross-Validation (Çapraz Doğrulama) ile Model İstikrarı

Eğitim seti SMOTE ile dengelendikten sonra, modelin performansının tesadüfi bir veri bölünmesine bağlı olup olmadığını test etmek için **5-Fold Stratified Cross-Validation** (5 Katlı Çapraz Doğrulama) uygulanmıştır.

- **CV Accuracy Skorları:** `[0.9827, 0.9819, 0.9790, 0.9786, 0.9771]`
- **Ortalama Accuracy:** `0.9799 (+/- 0.0042)`

**Yorum:** 5 farklı eğitim-test senaryosunda da modelin doğruluğu %97.7 ile %98.2 arasında kalmıştır. Standart sapmanın son derece düşük olması (`0.0042`), modelin verinin hangi kısmıyla eğitilirse eğitilsin çok istikrarlı (stable) sonuçlar ürettiğini ve şans faktöründen bağımsız çalıştığını raporlamaktadır.

---

### 3. SMOTE Kullanımının Model Güvenilirliğine Etkisi

Sentetik veri üretme tekniği olan SMOTE'un modele etkisi, sadece basit bir skor artışı olarak değil, **"iş birimi güvenilirliği"** açısından değerlendirilmiştir.

- **SMOTE Olmadan (Dengesiz Veri):** Recall: %89.23 | Precision: %90.06
- **SMOTE İle (Dengeli Veri):** Recall: %90.15 | Precision: %84.68

**Yorum:** Sadece salt skorlara (Accuracy) bakıldığında dengesiz veri seti daha yüksek bir Precision (Yanlış alarm vermeme) sunuyor gibi görünebilir. Ancak *iş modeli güvenilirliği (Business Reliability)* açısından asıl amaç, kurumun kaybedeceği müşterileri bulmaktır. Banka için potansiyel olarak gidecek bir müşteriyi gözden kaçırmak (False Negative), kalacak bir müşteriyi yanlışlıkla aramaktan (False Positive) finansal olarak çok daha zararlıdır. SMOTE kullanımı, modelin "Gerçek Churn" vakalarını yakalama yeteneğini (Recall) artırmış, modeli iş hedefleri doğrultusunda **daha güvenilir ve riskten kaçınan (risk-averse)** bir hale getirmiştir.

---

### 4. Threshold (Eşik Değer) Kararının Metriklere Etkisi ve Karmaşıklık Matrisi (Confusion Matrix)

Modelin tahmin olasılıklarını "Gidecek" veya "Kalacak" olarak ayırdığı sınır çizgisi (Threshold) farklı değerlerde test edilmiş ve ortaya çıkan somut iş sonuçları (Karmaşıklık Matrisi) incelenmiştir:

- **Eşik 0.30:** Recall %92.62 | Precision %82.47 *(Final Modelimizde Baz Alınan Mantık)*
  - *Matris:* 301 Doğru Yakalanan, **24 Kaçırılan Müşteri (FN)**, 64 Yanlış Alarm (FP)
- **Eşik 0.40:** Recall %90.15 | Precision %84.68
  - *Matris:* 293 Doğru Yakalanan, **32 Kaçırılan Müşteri (FN)**, 53 Yanlış Alarm (FP)
- **Eşik 0.50:** Recall %88.31 | Precision %87.23
  - *Matris:* 287 Doğru Yakalanan, **38 Kaçırılan Müşteri (FN)**, 42 Yanlış Alarm (FP)
- **Eşik 0.60:** Recall %87.08 | Precision %90.71
  - *Matris:* 283 Doğru Yakalanan, **42 Kaçırılan Müşteri (FN)**, 29 Yanlış Alarm (FP)

**Özet:** Eşik değeri düşürüldükçe model daha "şüpheci" davranarak daha çok müşteriyi riskli olarak etiketlemektedir. Örneğin eşiği 0.40'tan 0.30'a çektiğimizde, yanlışlıkla aradığımız müşteri sayısı 53'ten 64'e çıkmış (sadece 11 ek çağrı/operasyon maliyeti oluşmuş), ancak bunun karşılığında bankayı tamamen terk edecek olan **fazladan 8 müşteriyi daha** (Kaçırılanlar 32'den 24'e düşmüş) kurtarma şansı elde edilmiştir. Müşteriyi elde tutma (retention) kampanyası kapsamında 11 kişiyi fazladan aramanın maliyeti, kaybedilecek 8 müşterinin bankaya vereceği kalıcı finansal zarardan (FN maliyetinden) çok daha küçük olduğu hesaplanmıştır. **Bu nedenle projenin başlangıç aşamasında eşik değer olarak 0.40 düşünülmüş olsa da, yapılan bu ampirik dayanıklılık testi sonucunda 0.30 eşik mantığının banka için çok daha kârlı bir nokta (sweet spot) olduğu kanıtlanmış ve nihai karar 0.30 olarak güncellenmiştir.**

---

### 5. Modelin Başarısız Olabileceği Durumlar (Model Limitasyonları)

Makine öğrenmesi modelleri geçmişten öğrenir. Bu modelin gerçek hayatta başarısız olabileceği veya performansının düşebileceği senaryolar şunlardır:
1. **Ani Dışsal Şoklar:** Makroekonomik krizler, hiperenflasyon dönemleri veya rakiplerin çok agresif bir faiz/kredi kampanyası başlatması durumunda model, geçmiş veride bu durumu görmediği için yanılacaktır.
2. **Statik Yapı:** Model anlık (real-time) bir yapıda değildir. Müşterinin son 1 haftadaki ani harcama değişikliklerini yakalayamaz. Eğitildiği veri setindeki 12 aylık periyotlara bağımlıdır.
3. **Konsept Kayması :** Müşteri davranışları zamanla değişir (Örn: Dijital kanalların daha yaygınlaşması). Model 3-6 ayda bir yeniden güncel veriyle eğitilmezse (retrain) başarısı kademeli olarak düşecektir.

---

### 6. Veri Setinin Gerçek Hayatı Temsil Etme Limitasyonları

Bu projedeki veri setinin kısıtlamaları şu şekildedir:
1. **Zaman Serisi (Time-Series) Eksikliği:** Veri setinde "Toplam İşlem Sayısı" (Total_Trans_Ct) gibi kümülatif değerler vardır. Ancak bu işlemlerin "Hangi aylarda nasıl bir trend izlediği" (örneğin son 3 ayda sürekli mi düştü?) bilinememektedir. Bu da tahmin gücünü kısıtlamaktadır.
2. **Davranışsal ve Niteliksel Veri Eksikliği:** Müşteri hizmetlerini arama sıklığı, şikayet kayıtları (NLP ile analiz edilecek metinler) veya mobil uygulama kullanım logları gibi gerçek hayatta churn için en belirleyici olan veriler veri setinde yoktur.
3. **Survival (Sağ Kalım) Durumu:** Model sadece müşterinin gidip gitmeyeceğini sınıflandırır (Classification). Gerçek hayatta daha kritik olan "Müşterinin ne zaman / kaç ay sonra gideceği" sorusuna (Survival Analysis) cevap verebilecek nitelikte bir veri seti değildir.