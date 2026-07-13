---
marp: true
theme: gaia
class: lead
paginate: true
backgroundColor: #f8fafc
style: |
  section { justify-content: flex-start; padding: 50px; }
  h1 { color: #1e3a8a; font-size: 2.2em; text-align: center; margin-top: 150px; }
  h2 { color: #2563eb; font-size: 1.6em; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
  h3 { color: #0f172a; font-size: 1.3em; }
  p, li { color: #334155; font-size: 0.95em; line-height: 1.4; }
  .columns { display: flex; gap: 40px; align-items: center; margin-top: 20px; }
  .left { flex: 1.2; text-align: center; }
  .right { flex: 1; }
  .insight { background-color: #fee2e2; padding: 15px; border-left: 6px solid #dc2626; margin-top: 20px; font-weight: bold; color: #991b1b; border-radius: 4px; font-size: 0.9em; }
  img { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-height: 450px; }
  table { width: 100%; font-size: 0.7em; margin-top: 20px; }
  th { background-color: #f1f5f9; color: #0f172a; }
---

# Bankacılık Churn Analizi
**Kapsamlı Keşifçi Veri Analizi ve Veri Sözlüğü Raporu**

---
## Dataset Alternatifleri ve Seçim Gerekçesi

### 📉 Alternatif 1: Telco Customer Churn (Telekomünikasyon)
Genel Bakış: Telekomünikasyon sektörüne ait, 7,043 müşteri ve 21 özellik (feature) barındıran klasik bir veri setidir. Sektördeki ortalama churn oranı %26.5'tir.
- Avantajları: Veri seti oldukça temizdir ve veri bilimi projelerine yeni başlayanlar için makine öğrenmesi modellerini test etmek adına ideal bir temel oluşturur. Fatura türü, internet hizmetleri ve kontrat süresi gibi temel abonelik metriklerini içerir.
- Dezavantajları ve Elenme Sebebi: Çoğunlukla "Evet/Hayır" şeklindeki ikili (binary) kategorik değişkenlerden oluştuğu için derinlemesine istatistiksel ve finansal analize (örneğin limit kullanımı, harcama frekansı) izin vermez. Hedeflediğimiz ileri düzey analitik yetkinlikleri sergilemek için fazla basittir.

### 📦 Alternatif 2: E-commerce Customer Churn (E-Ticaret)
Genel Bakış: E-ticaret platformlarındaki kullanıcı alışkanlıklarını yansıtan, 5,630 müşteri ve 20 özellik içeren dinamik bir veri setidir. Churn oranı %16.8 civarındadır.
- Avantajları: Şikayet sayısı, depo uzaklığı, sipariş kategorisi gibi gerçek dünyadaki lojistik ve müşteri memnuniyeti operasyonlarını çok iyi yansıtır. Günlük hayatla kolayca bağdaştırılabilir.
- Dezavantajları ve Elenme Sebebi: İçerisinde çok ciddi oranda "Eksik Veri (Missing Value)" barındırır ve veri ön işlemesi (preprocessing) sırasında çok fazla yapay tahminleme gerektirir (Imputation). Odak noktamız eksik veri temizliğinden ziyade doğrudan var olan müşteri davranışlarının finansal analizi olduğu için bu set ikinci plana atılmıştır.

### 🏆 Seçilen Şampiyon Dataset: Credit Card Customers (Bankacılık)
Temel Problem Tanımı: Bankacılık sektöründe kredi kartı müşterilerinin kartlarını cüzdanın arka cebine atması (inaktif duruma geçmesi), ardından hesaplarını kapatması ve bankanın cüzdan payını (wallet share) rakip bankalara kaptırmasıdır.
- Boyut ve Çeşitlilik: 10,127 müşteri kaydı ile diğer alternatiflerden çok daha geniş bir gözlem havuzu sunar. Ayrıca 21 kolonun büyük çoğunluğu sürekli (continuous) sayısal değerlerdir, bu da daha zengin görselleştirmelere olanak tanır.
- Meydan Okuma (Imbalance): Sadece %16.1'lik ayrılma oranı ile gerçek hayata çok yakın ve zorlayıcı bir "Sınıf Dengesizliği (Class Imbalance)" problemi sunar. Bu durum, basit modellerin çökmesini sağlayarak SMOTE gibi ileri düzey veri sentezleme ve istatistiksel modelleme tekniklerini kullanmayı zorunlu kılar.
- Finansal Derinlik: Limit kullanım oranı (Utilization Ratio), devreden faizli bakiye (Revolving Balance) ve aylık işlem hacmi (Transaction Amount) gibi doğrudan bankanın gelirini ve karlılığını etkileyen, analiz etmesi son derece prestijli finansal metrikler barındırır.

### Yapay Zekanın Finansal Zirvesi: %91.6 Doğruluk
Karmaşık boyutlara sahip (Non-linear) bu finansal veriler üzerinde Destek Vektör Makineleri (SVM) %91.61 gibi inanılmaz bir Accuracy yakalamış, F1-Score ise 0.7176 olmuştur. Model API olarak entegre edilerek, aylık işlem adedi 44'ün altına inen ve arama sıklığı artan müşterileri anında VIP Retention (Müşteri Kurtarma) masasına aktaracak kapasitededir.

---
## Kritik Veri Sızıntısı (Data Leakage)
Veri setinin orijinal halinde Naive_Bayes_Classifier_Attrition_Flag_... isimli kolonlar bulunmaktadır. Bu kolonlar daha önceden eğitilmiş bir modelin "olasılık sonuçlarıdır" yani cevap anahtarıdır. Modelleme yapılmadan önce bu iki kolon ve CLIENTNUM (Müşteri ID) kolonu acımasızca silinerek (Drop) haksız bir %100 doğruluk engellenmiştir.

---
## 🎯 Target Değişkeni (Attrition_Flag)
Modelin tahmin etmeye çalıştığı ana hedef değişkendir. Müşterinin bankayı terk edip etmediğini gösterir:
- ✅ Existing Customer (Mevcut): 8,500 Müşteri (%83.9)
- ❌ Attrited Customer (Ayrılan): 1,627 Müşteri (%16.1)

---
## 🔍 Eksik Değer (Missing Value) ve Duplicate Kontrolü
Veri setinde tekrar eden (Duplicate) kayıt sayısı 0'dır. Standart (NaN) eksik değer bulunmamaktadır. Ancak bazı kategorik değişkenlerde müşteri bilgisi bilinmediği için "Unknown" olarak kaydedilmiş satırlar vardır:
- ❓ Education_Level: 1,519 satır 'Unknown' (%15.00)
- ❓ Income_Category: 1,112 satır 'Unknown' (%10.98)
- ❓ Marital_Status: 749 satır 'Unknown' (%7.40)

---
## ⚡ Veri Kalitesi İlk Bulguları
Keşifçi analiz öncesi ham veri üzerinde tespit edilen temel kalite ve yapı problemleri şunlardır:
- Sınıf Dengesizliği (Class Imbalance): %16.1 ayrılma oranı SMOTE uygulanmasını veya F1-Score kullanımını zorunlu kılar.
- Çoklu Doğrusallık (Multicollinearity): Credit_Limit ile Avg_Open_To_Buy arasında çok yüksek korelasyon tespit edilmiştir.
- Aykırı Değerler (Outliers): Özellikle Credit_Limit (%9.72) ve Total_Trans_Amt (%8.85) sütunlarında dağılımı bozan aykırı değerler mevcuttur.

---
## Veri Sözlüğü (Sayfa 1)

| Değişken | Tipi | Açıklama |
|---|---|---|
| **Attrition_Flag** | Target (Hedef) | Müşterinin bankayı terk edip etmediği. %83.9 Existing (Kalan), %16.1 Attrited (Giden). Modelin tahmin edeceği ana bağımlı değişkendir. |
| **Customer_Age** | Sayısal | Müşterinin demografik yaşı. Genellikle churn üzerinde anlamlı bir ayırt ediciliği bulunmamaktadır. |
| **Gender** | Kategorik | Müşterinin cinsiyeti (M: Erkek, F: Kadın). Kredi limitlerinde ufak farklar olsa da churn davranışını tek başına etkilemez. |
| **Dependent_count** | Sayısal | Bakmakla yükümlü olunan kişi/çocuk sayısı. Aile büyüklüğünü gösterir, ayrılan ve kalanlarda dağılım oldukça benzerdir. |
| **Education_Level** | Kategorik | Eğitim durumu (Lise, Üniversite, Doktora vb.). %15 oranında "Unknown" (Bilinmeyen) kategorisi barındırır. |

---
## Veri Sözlüğü (Sayfa 2)

| Değişken | Tipi | Açıklama |
|---|---|---|
| **Marital_Status** | Kategorik | Medeni durum (Evli, Bekar, Boşanmış vb.). %7.40 oranında eksik veriye ("Unknown") sahiptir. |
| **Income_Category** | Kategorik | Müşterinin yıllık gelir bandı. Müşteri kaybı, bankanın zengin veya düşük gelirli müşterilerinde benzer oranlarda görülmektedir. |
| **Card_Category** | Kategorik | Kartın prestij segmenti: Blue, Silver, Gold, Platinum. Sürpriz bir şekilde, en çok terk edenler %25 oranla Platinum sahipleridir. |
| **Months_on_book** | Sayısal | Bankayla çalışma süresi (kıdem). Yoğunluk 36 ay civarındadır. "Eski müşteri bankayı terk etmez" algısı bu veride geçersizdir. |
| **Total_Relationship_Count** | Sayısal | Müşterinin sahip olduğu farklı bankacılık ürünlerinin sayısı. Ürün sayısı (çapraz satış) azaldıkça sadakat kırılır, churn riski artar. |

---
## Veri Sözlüğü (Sayfa 3)

| Değişken | Tipi | Açıklama |
|---|---|---|
| **Months_Inactive_12_mon** | Sayısal | İşlem yapılmadan (inaktif) geçirilen ay sayısı. 3 ayı aştığında "Soft Churn" (uyku durumu) sinyali verir ve risk zirve yapar. |
| **Contacts_Count_12_mon** | Sayısal | Son 1 yılda banka ile kurulan temas/şikayet sayısı. En büyük churn tetikleyicilerinden biridir (+0.20 Pozitif Korelasyon). |
| **Credit_Limit** | Sayısal | Kredi kartı toplam limiti. Önceki analizlerde de görüldüğü gibi, limit yüksekliğinin müşteriyi bankaya bağlamakta doğrudan, tek başına bir gücü yoktur. |
| **Total_Revolving_Bal** | Sayısal | Hesap kesiminden sonra ödenmeyip faize bırakılan devreden bakiye. Bankanın ana gelir kalemidir. Borcunu faize bırakanlar bankaya daha sadıktır. |
| **Avg_Open_To_Buy** | Sayısal | Kredi limitinin harcanmayan, boşta kalan kullanılabilir kısmıdır. Credit_Limit ile tehlikeli derecede yüksek korelasyona sahiptir (Multicollinearity). |

---
## Veri Sözlüğü (Sayfa 4)

| Değişken | Tipi | Açıklama |
|---|---|---|
| **Total_Amt_Chng_Q4_Q1** | Sayısal | İşlem tutarlarının 1. çeyrekten 4. çeyreğe değişim oranı. Bu oran düştükçe çeyrekler arası harcama hacmi azalıyor demektir, ayrılma riskini artırır. |
| **Total_Trans_Amt** | Sayısal | Son 12 aydaki toplam harcama tutarı. Sağ çarpık bir dağılımı (Outliers) vardır, makine öğrenmesi öncesi Logaritmik dönüşüm veya Robust Scaler gerekebilir. |
| **Total_Trans_Ct** | Sayısal | Son 12 aydaki toplam işlem (harcama yapma) adedi. Harcama frekansını ölçer. Modelin açık ara en güçlü (-0.37 Negatif Korelasyon) sadakat belirleyicisidir. |
| **Total_Ct_Chng_Q4_Q1** | Sayısal | İşlem adetlerinin (frekans) 1. çeyrekten 4. çeyreğe değişim oranı. Düzenli kart kullanan müşteri kartı kullanma sıklığını azaltıyorsa bankayı terk etmeye hazırlanıyordur. |
| **Avg_Utilization_Ratio** | Sayısal | Limit Kullanım Oranı (Kullanılan Kredi / Toplam Limit). Ortalama kullanım kalan müşterilerde %30'lardayken, gidenlerde %16'lara sertçe düşmektedir. |

---
## 1 Genel Müşteri Kaybı (Churn) Oranı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 13.05.05.jpeg>)
</div>
<div class="right">
Pasta grafiği, veritabanındaki 10,127 müşterinin %16.1'inin ayrıldığını (Attrited), %83.9'unun ise mevcut müşteri olarak kaldığını göstermektedir. Bu oran, Makine Öğrenimi modellerini eğitirken ciddi bir sınıf dengesizliğine (Class Imbalance) işaret eder. SMOTE uygulanması zorunludur.
<div class="insight">Aksiyon: İşletme Riski: Dengesiz Veri Dağılımı</div>
</div>
</div>

---
## 2 Platin Segmentin (Platinum) Çöküşü

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 13.05.16.jpeg>)
</div>
<div class="right">
Kart segmentlerine göre ayrılma oranları incelendiğinde; Blue (Klasik) kart sahipleri %16.1, Silver %14.8 ve Gold %18.1 oranında iptal yaparken, Platinum kart sahiplerinin tam %25'i bankayı terk etmiştir. Üst gelir grubundaki bu müşteriler aşırı talepkardır ve rakip bankaların tekliflerine hızla geçiş yapmaktadır.
<div class="insight">Aksiyon: Strateji: VIP Masası Kurulumu</div>
</div>
</div>

---
## 3 Harcama Frekansı Gücü (Total_Trans_Ct)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 11.44.18.jpeg>)
</div>
<div class="right">
Kutu grafiğinde (Boxplot), bankada kalan müşterilerin (0) yıllık medyan işlem adedinin 70'lerde olduğu, ayrılan müşterilerin (1) ise işlem adedinin 40'lara çakıldığı net biçimde görülmektedir. Bankaya sadakati limit değil, kartın günde iki kez kahve almak gibi "sık" kullanılması sağlar. (-0.37 Negatif Korelasyon)
<div class="insight">Aksiyon: Strateji: Mikro-İşlem Oyunlaştırması</div>
</div>
</div>

---
## 4 İşlem Tutarı Dağılımı (Total_Trans_Amt)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 11.43.47.jpeg>)
</div>
<div class="right">
Ayrılan müşterilerin (1) 1 yıllık toplam harcama hacimleri de, işlem sayısına paralel olarak mevcut müşterilere (0) kıyasla dramatik seviyede düşüktür. Müşteri, ayrılmadan aylar önce harcamalarını (cüzdan payını) kademeli olarak rakip kuruma kaydırmaktadır (Soft Churn).
<div class="insight">Aksiyon: Bulgu: Cüzdan Payı (Wallet Share) Kaybı</div>
</div>
</div>

---
## 5 Müşteri Temsilcisi Tehlikesi (Contacts_Count)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 11.47.58.jpeg>)
</div>
<div class="right">
Mevcut müşterilerin çağrı merkezi arama medyanı 2 iken, ayrılanların medyanı 3'tür. Eğer bir müşteri yılda 3'ten fazla bankayı arıyorsa (üst kısımdaki aykırı değerlere doğru), bu bankaya bağlılık değil, çözülemeyen kronik bir şikayet göstergesidir. (+0.20 Pozitif Korelasyon - En Yüksek Risk)
<div class="insight">Aksiyon: Strateji: "Kırmızı Alarm" IVR Sistemi</div>
</div>
</div>

---
## 6 Pasif Kalma Süresi (Months_Inactive)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 11.51.08.jpeg>)
</div>
<div class="right">
Ayrılan müşterilerin dağılım kutusu belirgin şekilde yukarı (daha fazla inaktif ay) kaymıştır. Bir kredi kartı peş peşe 3 ay inaktif olduğunda, fiziksel olarak iptal edilmese bile finansal olarak çoktan ölü kabul edilmelidir.
</div>
</div>

---
## 7 Devreden Faizli Bakiye Paradoksu (Revolving Balance)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.50.46.jpeg>)
</div>
<div class="right">
Çubuk grafiği (Bar Chart) inanılmaz bir gerçeği gösteriyor: Tüm kart segmentlerinde mevcut müşteriler (Kırmızı) 1200$-1600$ civarı devreden bakiyeye sahipken, ayrılan müşterilerin (Mavi) devreden bakiyesi 500$ civarına iniyor. Hele ki Platinum ayrılanlarda bu değer neredeyse sıfır! Borcunu düzenli ödeyen disiplinli müşteriler, bankayı çok daha kolay terk eder.
<div class="insight">Aksiyon: Bulgu: Faiz Döngüsü Sadakati Bağlar</div>
</div>
</div>

---
## 8 Limit Kullanım Oranı (Utilization Ratio)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/14_DAGILIM_kullanim_orani.png>)
</div>
<div class="right">
Mevcut müşteriler kendilerine tanınan kredi limitinin ortalama %29.6'sını harcarken, ayrılan müşteriler (Kırmızı Dağılım Eğrisi sola çarpık) sadece %16.2'sini kullanmaktadır. Kullanılmayan devasa boş limitler, o müşterinin o bankaya ihtiyaç duymadığının kanıtıdır.
</div>
</div>

---
## 9 Kredi Limiti Yanılgısı (Gender / Credit Limit)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.41.49.jpeg>)
</div>
<div class="right">
Cinsiyet kırılımında bakıldığında erkek müşterilerin ortalama limiti kadınlara göre daha yüksek görünse de, Asıl Çıkarım: Churn olan müşterilerin (Mavi bar) limitleri, kalan müşterilerden (Kırmızı) neredeyse farksızdır. "Müşterinin limiti yüksek olsun iptal etmez" inanışı bir efsanedir.
</div>
</div>

---
## 10 Kıdem (Months on Book) Yanılgısı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/19_DAGILIM_musterilik_suresi.png>)
</div>
<div class="right">
Dağılım grafikleri, hem ayrılan hem de kalan müşterilerin yoğunlukla 36. ayda (3 yıl) toplandığını kanıtlıyor. Ortalama süreleri (36.1 ay vs 35.8 ay) arasında fark yoktur. Bankacılıkta "Eski müşteri bir yere gitmez" kuralı maalesef işlemiyor.
</div>
</div>

---
## 11 Gelir Sınıfından Bağımsız Harcama Düşüşü

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.31.48.jpeg>)
</div>
<div class="right">
Gelir kategorisi (Income_Category) "60K-80K" veya "+120K" olsun fark etmeksizin, tüm barlarda ayrılan müşterilerin (Mavi) işlem tutarları mevcutlardan (Kırmızı) düşüktür. Churn sinyali gelirden tamamen bağımsız, evrensel bir harcama kesintisi davranışıdır.
</div>
</div>

---
## 12 Cinsiyet Segmentinde İşlem Tutarı Dağılımı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.39.36.jpeg>)
</div>
<div class="right">
Ayrılan kadın ve erkek müşterilerin kutu grafikleri, mevcut müşterilere göre çok daha basık ve dar bir aralıktadır. Erkeklerde üst sınır (aykırı değerler hariç) 5000$ civarında ezilirken, kalan müşterilerde 10000$ sınırına kadar esneyebilmektedir.
</div>
</div>

---
## 13 Cinsiyet Segmentinde İşlem Adedi Dağılımı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.41.09.jpeg>)
</div>
<div class="right">
Kadınların ve erkeklerin "Kredi kartını slip çektirme sayıları" incelendiğinde; Churn statüsü (Mavi) tüm demografik ayrıcalıkları silip süpürerek işlem adetlerini 40 bandına çekmektedir. Cinsiyet sadakat sağlamaz, işlem adedi sağlar.
</div>
</div>

---
## 14 Kart Segmentine Göre Cüzdan Derinliği

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.43.24.jpeg>)
</div>
<div class="right">
En dramatik düşüş Platinum kartlarda görülür. Kalan bir Platinum müşteri yılda ortalama 10,000$ harcarken, ayrılacak olan Platinum müşterinin hacmi %50 azalarak 5,000$ altı seviyeye (Blue kart seviyesine) gerilemiştir.
<div class="insight">Aksiyon: Ani limit boşluklarında kampanya çıkılmalı</div>
</div>
</div>

---
## 15 Kart Segmentine Göre İşlem Frekansı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.46.11.jpeg>)
</div>
<div class="right">
Beklendiği üzere üst segment (Platinum, Gold) kartlar çok daha fazla işlem adetine sahip. Ancak, ayrılacak müşteriler için bu grafiğin tüm kutuları sabit bir ivmeyle aşağı çökmüştür.
</div>
</div>

---
## 16 Toplam Ürün (Relationship) Bağlılığı

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 11.46.43.jpeg>)
</div>
<div class="right">
Bankadan kaç farklı ürün kullanıldığı (Total_Relationship_Count). Kutu grafiği, ayrılan müşterilerin banka ile daha az bağa (medyan 3) sahip olduğunu gösteriyor. Sadece kredi kartı olanlar risklidir, mevduat ve otomatik ödeme eklenince sadakat artar.
</div>
</div>

---
## 17 Platin Segmentin İlginç Ürün Talebi

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.57.24.jpeg>)
</div>
<div class="right">
Barlar incelendiğinde; Blue, Silver ve Gold segmentlerinde ayrılan müşterilerin ürün sayısı daha AZ iken, Platinum segmentinde ayrılan müşterilerin ürün ortalaması mevcutlardan daha FAZLA çıkmıştır. Bu durum, Özel Bankacılık profilinin ürünlerden yeterince verim/ayrıcalık alamadığı için kızıp terk ettiğini ispatlar.
</div>
</div>

---
## 18 Kullanılabilir Açık Limit (Avg_Open_To_Buy)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.51.48.jpeg>)
</div>
<div class="right">
Limitin harcanmayan kısmı (Açık Limit) ayrılan müşterilerde, özellikle de yüksek segmentlerde daha yukarıdadır. Limitin kullanılmaması, o kartın "Cüzdanın Arka Cebine" atıldığını gösterir.
</div>
</div>

---
## 19 Kredi Limiti Dağılımı ve Churn Etkisi

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/15_DAGILIM_kredi_limiti.png>)
</div>
<div class="right">
Banka portföyünün büyük çoğunluğu $1,500 - $5,000 limitleri arasına yığılmıştır. Asıl önemli bulgu şudur: Kredi limitinin yüksekliği tek başına sadakati (churn durumunu) doğrudan etkilememektedir. Dağılım grafiği, hem ayrılan hem de kalan müşterilerin benzer limit eğrilerine sahip olduğunu gösteriyor. Bankaların müşteriyi tutmak için sadece limit artırımına gitmesi faydasız bir stratejidir.
</div>
</div>

---
## 20 Aile Büyüklüğü (Dependent_count)

<div class="columns">
<div class="left">
![auto](<GRAFİKLER/WhatsApp Image 2026-07-08 at 12.28.41.jpeg>)
</div>
<div class="right">
Bakmakla yükümlü olunan çocuk/kişi sayısının churn ile arasında belirgin bir ayrıştırıcı (discriminative) dağılım saptanamamıştır. Medyan değer her iki grupta da 2'dir.
</div>
</div>