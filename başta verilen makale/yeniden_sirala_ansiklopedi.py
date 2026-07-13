import os
import markdown
from playwright.sync_api import sync_playwright

md_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.md'
html_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.html'
pdf_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.pdf'

# Clear the file first
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# Makine Öğrenmesi & CLV Ansiklopedisi: Tam Kapsamlı Mantık Rehberi\n\n")

def append_to_md(content):
    with open(md_file, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")

# 1
append_to_md("""
## BÖLÜM 1: Makalelerin Özü ve Makine Öğrenmesinin Amacı

Bu klasördeki makalelerde (özellikle Vafeiadis vd., 2015 ve Lalwani vd., 2021) dünyadaki **tüm klasik ve modern makine öğrenmesi modelleri** (SVM, Naive Bayes, Lojistik Regresyon, KNN, ANN, Karar Ağaçları, Boosting vb.) müşteri kaybını (churn) tahmin etmek için adeta birbiriyle dövüştürülür. 

Peki neden bu kadar çok model var? Çünkü makine öğrenmesi dediğimiz şey sihir değildir; verinin (müşterilerin) arasına çizgi çekme sanatıdır. Kimi model bu çizgiyi düz çeker, kimi yuvarlak çizer, kimi ise boyutu büker. Şimdi bu makalelerde adı geçen HER BİR MODELİN ne olduğunu, nasıl çalıştığını ve arka planındaki matematiği **tamamen bakkal, zar atma ve günlük hayat örnekleriyle**, birbirini takip eden bir sırayla en ince ayrıntısına kadar inceleyelim.
""")

# 2
append_to_md("""
## BÖLÜM 2: K-En Yakın Komşu (KNN) Algoritması

En ilkel ama en etkili tahmin modellerinden biri **KNN (K-Nearest Neighbors)** algoritmasıdır. Herhangi bir denklem çözmez.

**Mantığı (Bana Arkadaşını Söyle):**
Yeni bir müşteri geldi. Acaba bizi terk edecek mi (Churn) yoksa kalacak mı (Sadık)? 
KNN algoritması bu yeni müşteriyi alır ve devasa veri tabanındaki diğer müşterilerin arasına (bir haritaya) koyar. Sonra **K** harfi ile belirtilen sayıda en yakın komşusuna bakar. 
Eğer K=5 seçtiysek, makine bu yeni müşterinin haritadaki en yakın 5 komşusuna (yani harcama alışkanlıkları, yaşı ve faturası bu müşteriye en çok benzeyen 5 kişiye) bakar.
- Eğer o 5 komşunun 4'ü geçmişte bizi terk etmişse, makine der ki: *"Bana arkadaşını söyle sana kim olduğunu söyleyeyim. Senin en çok benzediğin 5 adamın 4'ü gitmiş. Demek ki sen de gideceksin!"*

**Zayıflığı:** Veri tabanınızda 1 milyon müşteri varsa, yeni gelen adamı her seferinde 1 milyon kişiyle tek tek karşılaştırıp mesafesini (Pisagor teoremiyle) ölçmek zorundadır. Dev şirketlerde yavaş kalır.
""")

# 3
append_to_md("""
## BÖLÜM 3: Naive Bayes (Olasılıksal Sınıflandırma)

**Mantığı (Dedektiflik ve Masum İhtimaller):**
Siz bir dedektifsiniz. Olay yerinde 3 ipucu var: Sigara izmariti, kırmızı ruj ve 44 numara ayak izi. Amacınız katilin "Erkek" mi "Kadın" mı olduğunu bulmak.
Naive Bayes, her ipucunu TEK TEK hesaplar:
- Sigara izmariti erkeklerde %60, kadınlarda %40 görülür.
- Kırmızı ruj kadınlarda %99, erkeklerde %1 görülür.
- 44 numara ayak izi erkeklerde %95, kadınlarda %5 görülür.

Model bu olasılıkları (Bayes teoremiyle) birbiriyle çarpar ve sonuca ulaşır. 
Telekom şirketlerinde de durum aynıdır. Müşterinin faturası (ipucu 1) ve sözleşme süresi (ipucu 2) çarpılarak "Terk Etme Olasılığı" bulunur. 
**Zayıflığı:** Adındaki "Naive" (Saf) kelimesi şuradan gelir: Model, kırmızı ruj ile 44 numara ayak izinin aynı anda bulunmasının ne kadar mantıksız (birbiriyle ilişkili) olduğunu kavrayamaz. Her şeyi birbirinden tamamen bağımsız sanıp dümdüz çarpar.
""")

# 4
append_to_md("""
## BÖLÜM 4: Lojistik Regresyon (İhtimalleri Bükmek)

Klasik istatistiğin bel kemiği olan Lojistik Regresyon, makalelerde sıkça Karar Ağaçlarına rakip olarak çıkar. Adında "regresyon" (gelecekteki satış rakamını tahmin etme) geçse de aslında bu bir **Sınıflandırma (Churn olur/olmaz)** algoritmasıdır.

**Mantığı ("S" Şeklinde Esnek Çizgi):**
Diyelim ki x ekseninde müşterinin yaşı, y ekseninde "Churn oldu(1) / Olmadı(0)" yazıyor. Normal bir doğru çizerseniz, çizgi 0'ın altına veya 1'in üstüne taşar (Olasılık %120 veya eksi %20 olamaz!).
Lojistik regresyon matematiksel bir sihir kullanır ve o dümdüz çizgiyi **"S" harfi şeklinde büker (Sigmoid Fonksiyonu)**.
Bu "S" eğrisi 0 ile 1 arasına sıkışmıştır. Bir müşterinin verisini modele verdiğinizde size "Kesin churn olur" demez. "Bu müşterinin churn olma ihtimali %73'tür" der. Şirketler için harikadır çünkü müşterileri ihtimallerine göre sıraya dizmenizi sağlar.
""")

# 5
append_to_md("""
## BÖLÜM 5: Karar Ağaçları (Decision Trees) ve Soru Seçimi

Model açıklanabilirliği istendiğinde şirketlerin en sevdiği modeldir. Lojistik Regresyon gibi formül çözmez, "MANTIK" yürütür.

**Mantığı (Bakkalın Zihin Haritası):**
Bakkal Ahmet Amca'nın "Borç Verilir mi?" haritasıdır.
1. "Bu adam mahalleden mi?" (Evet -> Alt dala in. Hayır -> Verme).
2. "Geçen aydan borcu var mı?" (Evet -> Verme. Hayır -> Ver).

Telekomda da ağaç yukarıdan aşağıya (Kontrat süresi? Fiber mi? Şikayet kaydı var mı?) inerek müşteriyi sepetlere atar.

### 5.1. Ağaç İlk Soruyu Neye Göre Seçer? (Gini Index ve Information Gain)
Peki bilgisayar ağacın EN TEPESİNE hangi soruyu koyacağına nasıl karar veriyor? Neden "Ayakkabı numarası kaç?" sorusunu en tepeye koymuyor da "Sözleşme tipi nedir?" sorusunu koyuyor?
İşte bunu **Gini Safsızlığı (Impurity)** ve **Bilgi Kazancı (Information Gain)** ile hesaplar.

**Örnek (Kırmızı ve Mavi Topları Ayırmak):**
Elinizde içinde 50 Kırmızı (Churn) ve 50 Mavi (Sadık) top olan bir sepet var. Bu sepet **çok kirlidir (Gini Impurity yüksektir)** çünkü her şey birbirine karışmıştır.
Ağaç tüm soruları dener. 
- Eğer "Cinsiyeti erkek mi?" sorusunu sorarsa, toplar "40 Kırmızı-45 Mavi" ve "10 Kırmızı-5 Mavi" diye ayrılır. Kirlilik pek azalmamıştır.
- Ama "Aylık sözleşmesi mi var?" diye sorarsa, toplar "48 Kırmızı - 2 Mavi" ve "2 Kırmızı - 48 Mavi" diye ayrılır! Gördünüz mü? Sepetler neredeyse "saf" (tertemiz) renklerine ayrıldı.
Ağaç, sepeti en temiz (saf) hale getiren, kirliliği (Gini'yi) en çok düşüren veya bize en çok Bilgi Kazancı (Information Gain) sağlayan soruyu bulur ve EN TEPEYE o soruyu çakar.
""")

# 6
append_to_md("""
## BÖLÜM 6: Rastgele Orman (Random Forest)

Karar ağaçları çok güzeldir ama bazen bir istisnayı kural sanıp veriyi ezberlerler (Overfitting). 

**Mantığı (Bin Doktorluk Demokrasi Heyeti):**
Eğer hastaysanız tek bir doktora (Tek Karar Ağacı) güvenirseniz hata yapabilirsiniz. Random Forest, veriyi rastgele binlerce parçaya böler ve 1.000 farklı zayıf doktor (ağaç) yaratır.
Siz odaya girdiğinizde 1.000 ağaç birden OY KULLANIR. 
800 ağaç "Churn", 200 ağaç "Sadık" derse çoğunluk kazanır! Birkaç ağaç saçma sorular sorup hata yapsa bile, demokrasinin gücü (Ensemble Learning) o hatayı yutar. Bu yüzden churn tahmininde daima en sağlam (robust) sonuçları verir.
""")

# 7
append_to_md("""
## BÖLÜM 7: Destek Vektör Makineleri (SVM) ve Kernel Hilesi

Makalelerde (Vafeiadis vd.) tüm algoritmaları yok eden o meşhur modele geldik. 

**Mantığı (Çelikten Duvar Örmek):**
Masanın üzerinde Kırmızı (Churn) ve Mavi (Sadık) misketler var. Amacımız masaya dümdüz bir cetvel koyup bunları ikiye ayırmak. SVM, cetveli koyarken en uçtaki misketlere en uzak olacak şekilde, yolun ortasına çelik bir duvar (Hyperplane) örer.

**Peki Ya Misketler İç İçe Geçmişse? (Kernel Trick / Çekirdek Hilesi):**
Veri her zaman cetvelle ayrılacak kadar dümdüz (Linear) değildir. SVM'in sihri buradadır. Eğer veriyi ayıramıyorsa, **"Kernel Trick"** denen matematiği kullanır. 
Masaya alttan çok sert bir yumruk attığınızı düşünün! Misketler havaya zıplar (Veri 2 boyuttan 3 boyuta, uzaya çıkar). SVM misketler havadayken aralarından düz bir tepsi geçirir. Misketler masaya düştüğünde, o dümdüz tepsi masada harika bir daire (RBF Kernel) veya kıvrımlı bir S (Polynomial Kernel) şeklinde görünür. 
Makaledeki araştırmacılar veriyi havalandırmak için **SVM-POLY (Polinom)** kullanarak o çelik duvarı çekmiş ve muazzam başarı yakalamıştır.
""")

# 8
append_to_md("""
## BÖLÜM 8: Yapay Sinir Ağları (ANN) - Kara Kutu

Beynimizin çalışmasını taklit eden algoritmadır. 
Fatura, yaş ve kontrat bilgileri elektrik sinyali olarak ağa girer. İçeride gizli nöronlar (Hidden Layers) vardır. "Fatura yüksekse ve yaş gençse A nöronunu ateşle!" mantığıyla sinyaller katmanlar arası geçer, sona ulaşır ve "Churn!" diye bağırır.

**Sorunu (Kara Kutu - Black Box):** Çok başarılıdır ancak bir banka müdürü "Bu müşteri neden bizi bırakıyor?" dediğinde ANN size Karar Ağaçları gibi "Çünkü aylık kontratı var" demez. "İçerideki 453. nöron ateşlendiği için" der. Kimse bunu anlamadığı için ticari hayatta aksiyon alması zor bir modeldir.
""")

# 9
append_to_md("""
## BÖLÜM 9: AdaBoost ve XGBoost (Zayıflardan Ordu Kurmak)

Vafeiadis makalesinde SVM kendi başına %92 başarı verirken, bunu **AdaBoost** ile birleştirmişler ve oranı **%96.85'e** uçurmuşlardır!

**Mantığı (Hatalardan Ders Almak):**
Random Forest ağaçları "Aynı anda" oy kullanır. AdaBoost ise "Sırayla" çalışır.
1. Çok aptal bir ağaç (sadece 1 soruluk) kurulur. 100 müşteriden 70'ini bilir, 30'unu yanlış tahmin eder.
2. **Sihir:** AdaBoost, o YANLIŞ bilinen 30 müşterinin ağırlığını (kırmızı kalemle altını çizerek) devasa artırır.
3. İkinci aptal ağaca der ki: "Öncekileri boşver, sen sadece şu kırmızı zor müşterilere odaklan!" İkinci ağaç o 30 kişiden 20'sini bilir, 10'unu bilemez.
4. O 10 kişinin puanı daha da artırılıp üçüncü ağaca verilir.

Böyle böyle hatalardan ders alan yüzlerce model arka arkaya dizilir. Sonunda bu aptallar ordusu birleştiğinde (XGBoost/AdaBoost), hiçbir zor müşteriyi kaçırmayan dünyanın en güçlü algoritmasına dönüşür.
""")

# 10
append_to_md("""
## BÖLÜM 10: Makineyi Sınava Sokmak (Overfitting ve Çapraz Doğrulama)

Makine modellerini eğittik. Peki makinenin zeki mi olduğunu, yoksa sorunun cevaplarını papağan gibi ezberlediğini mi nasıl anlayacağız?

### 10.1. Overfitting (Ezberlemek) ve Underfitting (Aptallık)
- **Underfitting:** Makine veriyi hiç öğrenememiştir. "Herkes churn olacak" diyip geçer. Aptaldır.
- **Overfitting (Aşırı Öğrenme):** Makine veriyi o kadar iyi ezberler ki (başarı %100 çıkar), ancak dışarıdan yepyeni bir müşteri geldiğinde çuvallar. Tıpkı matematik deneme sınavının cevap anahtarını ezberleyen ama gerçek sınavda sıfır alan öğrenci gibi.

### 10.2. Çapraz Doğrulama (K-Fold Cross Validation)
Makinenin ezberlemesini engellemek için onu 10 farklı deneme sınavına sokarız. (Örn: 10-Fold CV).
Veriyi 10 eşit parçaya (kitapçığa) böleriz. Makine 9 parçayla ders çalışır (Train), daha önce HİÇ GÖRMEDİĞİ 10. parçayla sınava girer (Test). 
Sonra bunu 10 kez döndürürüz, her defasında farklı bir parçayla sınava sokarız. Eğer makine 10 sınavın ortalamasında da başarılıysa, o zaman gerçekten "Zeki" olduğuna (Generalization) ikna oluruz. Makalelerdeki tüm başarı oranları bu Çapraz Doğrulamadan geçmiştir.
""")

# 11
append_to_md("""
## BÖLÜM 11: Başarı Yanılsaması (Neden %99 Doğruluk Şirketi Batırır?)

İşte makalelerdeki en kritik kavramlara (Confusion Matrix, Precision, Recall, F1-Score, ROC/AUC) geldik. Churn verisi dengesizdir (10.000 müşterinin sadece 500'ü gider).
Eğer algoritma tembellik yapıp "Bütün müşteriler KALACAK" diye tahmin ederse, 9.500 kişiyi doğru bilmiş olur. **Accuracy (Doğruluk) oranı %95 çıkar!**
Siz %95'i görüp havalara uçarsınız ama makine asıl bulması gereken o 500 kaçağın hiçbirini (SIFIR) bulamamıştır! Şirketiniz batar. Bu tuzağa düşmemek için **Karmaşıklık Matrisi (Confusion Matrix)** kullanılır.

### 11.1. Recall (Duyarlılık - Avı Kaçırmamak)
Gerçekte giden 500 kişinin kaçını yakalayabildiniz? %10 mu? O zaman Accuracy %95 olsa da Recall'unuz yerlerdedir! Telekom şirketleri Recall'u yüksek ister, çünkü gideni bulmak (tehlikeyi kaçırmamak) esastır. Tıpkı kanser taraması gibi, kimseyi gözden kaçırmamalısınız.

### 11.2. Precision (Kesinlik - Attığını Vurmak)
Sisteminiz 100 kişiye "Bunlar gidiyor!" diye alarm verdi. Baktınız, sadece 20'si gerçekten gidiyor, 80'i halinden memnun yalan alarm (False Positive). Precision'ınız çok düşüktür. Boş yere o 80 kişiye hediye çeki verip şirketi zarara sokarsınız.

### 11.3. F1-Score ve ROC/AUC
- **F1-Ölçütü:** Precision ile Recall arasında bir orta yol (Harmonik ortalama) bulur. Hem attığımı vurayım, hem de kimseyi gözden kaçırmayayım. Modellerin asıl başarı karnesi budur.
- **ROC/AUC:** Hastanelerdeki ultrason cihazının hassasiyet ayarı gibidir. Alarmı çok öttürürseniz (herkese churn derseniz) kimseyi kaçırmazsınız ama boşuna para harcarsınız. İkisinin dengesini kuran harika bir eğridir.
""")

# 12
append_to_md("""
## BÖLÜM 12: 6 Aşamalı Churn Tahmin Fabrikası ve SMOTE

Praveen Lalwani (2021) makalesindeki IBM Watson altyapısı nasıl kurulur? Modeller havada uçuşmuyor, bu bir fabrikadır.
1. **Veri Seçimi:** Ham veriyi çekmek.
2. **Ön İşleme (Preprocessing):** Boş verileri doldurmak, Erkek/Kadın yerine 1/0 yazmak.
3. **Özellik Seçimi (Feature Selection):** "Ayakkabı numarası churn'ü etkilemez" deyip o veriyi çöpe atmak.
4. **Sentetik Veri Üretimi (SMOTE):** Verinin dengesiz (9500 İyi / 500 Kötü) olduğunu söylemiştik. Veri bilimciler o 500 kötü müşterinin DNA'sını kopyalayıp bilgisayarda 9.000 tane SAHTE (Sentetik) kötü müşteri klonlarlar. Makine artık 9500 İyi ve 9500 Kötü müşteriyi masada görünce eşit derecede çalışmak zorunda kalır!
5. **Model Eğitimi:** Karar Ağacı, SVM veya KNN burada çalışır.
6. **Değerlendirme:** Recall ve F1-Score'a bakılarak modelin onayı verilir.
""")

# 13
append_to_md("""
## BÖLÜM 13: ASOS.com ve "Embedding" (Tarzı Matematiğe Dökmek)

E-ticaret devi ASOS.com'un Müşteri Yaşam Boyu Değerini (CLV) nasıl bulduğuna gelelim. ASOS 85.000 ürünü olan dev bir şirkettir. Ve modellerini sadece "Müşteri ne kadar harcadı?" sorusuna göre değil, **"Müşteri ne TARZ harcadı?"** sorusuna göre kurarlar.

**Word2Vec'ten Ürün Uzayına:**
Bilgisayar "Deri Ceket"in veya "Hasır Şapka"nın ne olduğunu bilmez. ASOS veri bilimcileri, alışveriş sepetlerini bir "cümle" gibi inceler. 
Müşteri hep Siyah Kot ile Deri Ceket'i aynı sepete atıyorsa, bilgisayar bu iki kıyafeti 3 Boyutlu devasa bir uzayda birbirine çok yakın bir yere konumlandırır (Embedding / Gömme). Hasır şapkayı ise uzayın öbür ucuna koyar.

Sonra algoritma "Müşteriyi" bu uzayın içine fırlatır! Müşteri uzayda hangi kıyafetlerin yanına düşerse, onun profili (iade yapma ihtimali, sadakati) o kıyafetlerin karakterine bürünür.
Model (Random Forest), müşterinin harcadığı paraya değil, uzaydaki bu koordinatlarına bakarak tahmini yapar.
""")

# 14
append_to_md("""
## BÖLÜM 14: Sonuç ve En Büyük Çıkarımlar

Bu klasördeki makaleler bize veri biliminin şu kuralını öğretir: **Her araba her yolda sürülmez.**

1. Eğer elinizde "Ahmet neden iptal etti?" sorusunun cevabını yöneticinize açıklamanız gereken bir sunum varsa, ASOS.com'un uzay vektörlerini veya ANN'yi kullanamazsınız. Anlatılabilecek tek şey **Karar Ağaçlarıdır.** 
2. "Ben nedenini umursamıyorum, yeter ki kimin iptal edeceğini en yüksek isabetle bileyim" diyorsanız, Hatalardan ders alan **AdaBoost/XGBoost** veya Bin doktorluk heyet **Random Forest** kullanmalısınız.
3. Eğer elinizdeki veri çok dengesizse algoritmayı kurmadan önce mutlaka **SMOTE** ile sahte kötü müşteriler üretip veriyi teraziye sokmalısınız.
4. Bir modelin **Accuracy (Doğruluk) oranı %99** ise orada alkışlamayın, şüphelenin! Makine ya veriyi ezberlemiştir (Overfitting - K-Fold ile test edilmemiştir) ya da sadece çoğunluğu söyleyip azınlığı kaçırıyordur. Yöneticinin her zaman sorması gereken soru şudur: *"Doğruluğu geç, benim Recall ve F1 Skorum kaç?"*
""")

print("Markdown content logically sequenced and written.")

# Read the generated markdown
with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Convert to HTML
html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])

# Make blockquotes out of standard quotes
html_content = html_content.replace('<blockquote>', '<blockquote class="premium-quote">')

# Professional CSS Template
css_template = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Ansiklopedik Makine Öğrenmesi Rehberi</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Open+Sans:wght@400;600;700;800&display=swap');
        
        :root {
            --primary-dark: #0f172a; 
            --primary: #1e293b; 
            --accent: #2563eb; 
            --accent-light: #eff6ff;
            --text-main: #1e293b;
            --bg-main: #ffffff;
            --border-light: #cbd5e1;
            --surface: #f8fafc;
        }

        body {
            font-family: 'Merriweather', serif;
            color: var(--text-main);
            background-color: var(--bg-main);
            line-height: 1.8;
            font-size: 11.5pt;
            margin: 0;
            padding: 0;
            text-align: justify;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Open Sans', sans-serif;
            color: var(--primary-dark);
            font-weight: 800;
            line-height: 1.4;
        }

        .cover-page {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            page-break-after: always;
            padding: 50px;
            box-sizing: border-box;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            position: relative;
        }
        
        .cover-border {
            position: absolute;
            top: 25px;
            left: 25px;
            right: 25px;
            bottom: 25px;
            border: 4px solid var(--primary-dark);
            z-index: 1;
        }

        .cover-inner {
            position: absolute;
            top: 35px;
            left: 35px;
            right: 35px;
            bottom: 35px;
            border: 1px dashed var(--accent);
            z-index: 1;
        }

        .cover-content {
            z-index: 2;
            padding: 50px;
            background: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            max-width: 85%;
        }

        .cover-title {
            font-size: 34pt;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 25px;
            color: var(--primary-dark);
        }
        
        .cover-divider {
            height: 6px;
            width: 120px;
            background-color: var(--accent);
            margin: 0 auto 35px auto;
        }

        .cover-subtitle {
            font-family: 'Merriweather', serif;
            font-size: 15pt;
            font-style: italic;
            color: #475569;
            margin-top: 0;
            line-height: 1.7;
        }
        
        .cover-author {
            margin-top: 50px;
            font-family: 'Open Sans', sans-serif;
            font-size: 13pt;
            font-weight: 800;
            color: white;
            letter-spacing: 2px;
            background: var(--primary-dark);
            padding: 12px 30px;
            display: inline-block;
        }

        .content {
            padding: 0;
        }
        
        .content > h1:first-child {
            display: none;
        }

        h2 {
            font-size: 21pt;
            margin-top: 60px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--primary-dark);
            page-break-before: always;
            color: var(--primary-dark);
            text-transform: uppercase;
        }
        
        .content > h2:first-of-type {
            page-break-before: auto;
        }

        h3 {
            font-size: 16pt;
            margin-top: 40px;
            margin-bottom: 15px;
            color: var(--primary);
            border-left: 5px solid var(--accent);
            padding-left: 15px;
            background: var(--surface);
            padding-top: 10px;
            padding-bottom: 10px;
        }

        p {
            margin-bottom: 18pt;
        }

        blockquote, .premium-quote {
            background-color: var(--surface);
            border-left: 6px solid var(--accent);
            padding: 20pt;
            margin: 30pt 0;
            font-size: 12pt;
            font-style: italic;
            color: var(--primary-dark);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        ul, ol {
            padding-left: 30pt;
            margin-bottom: 25pt;
        }

        li {
            margin-bottom: 12pt;
        }

        strong {
            font-family: 'Open Sans', sans-serif;
            font-weight: 700;
            color: var(--primary-dark);
        }
    </style>
</head>
<body>
    <div class="cover-page">
        <div class="cover-border"></div>
        <div class="cover-inner"></div>
        <div class="cover-content">
            <div class="cover-title">Makine Öğrenmesi & CLV Ansiklopedisi</div>
            <div class="cover-divider"></div>
            <div class="cover-subtitle">Karar Ağaçlarından SVM'e, Performans Tuzaklarından Algoritma Kıyaslamalarına "Bakkal Mantığıyla" Kusursuz Rehber</div>
            <div class="cover-author">TAM KAPSAMLI LİTERATÜR (TÜM MODELLER VE METRİKLER)</div>
        </div>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""

full_html = css_template.replace('{content}', html_content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("HTML created, starting Playwright PDF generation...")

header_template = "<span></span>"
footer_template = """
<div style="font-size: 11px; color: #64748b; font-family: 'Open Sans', sans-serif; text-align: center; width: 100%; border-top: 1px solid #e2e8f0; padding-top: 8px; margin: 0 25mm;">
    Makine Öğrenmesi & CLV Ansiklopedisi | Sayfa <span class="pageNumber"></span> / <span class="totalPages"></span>
</div>
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///' + html_file.replace('\\', '/'))
    
    page.evaluate("document.fonts.ready")
    
    page.pdf(
        path=pdf_file, 
        format='A4', 
        print_background=True, 
        display_header_footer=True,
        header_template=header_template,
        footer_template=footer_template,
        margin={'top':'30mm', 'right':'25mm', 'bottom':'30mm', 'left':'25mm'}
    )
    browser.close()

print("Logical Sequenced Ansiklopedik ML PDF created successfully!")
