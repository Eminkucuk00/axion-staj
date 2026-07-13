import os
import markdown
from playwright.sync_api import sync_playwright

md_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.md'
html_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.html'
pdf_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.pdf'

# Clear the file first
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# Gerçek Makine Öğrenmesi Ansiklopedisi: Bütün Modeller ve İspatları\n\n")

def append_to_md(content):
    with open(md_file, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")

# CHAPTER 1
append_to_md("""
## BÖLÜM 1: Makalelerin Özü ve Makine Öğrenmesinin Amacı

Bu klasördeki makalelerde (özellikle Vafeiadis vd., 2015 ve Lalwani vd., 2021) dünyadaki **tüm klasik ve modern makine öğrenmesi modelleri** (SVM, Naive Bayes, KNN, ANN, Karar Ağaçları, Boosting vb.) müşteri kaybını (churn) tahmin etmek için adeta birbiriyle dövüştürülür. 

Peki neden bu kadar çok model var? Çünkü makine öğrenmesi dediğimiz şey sihir değildir; verinin (müşterilerin) arasına çizgi çekme sanatıdır. Kimi model bu çizgiyi düz çeker, kimi yuvarlak çizer, kimi ise boyutu büker. Şimdi bu makalelerde adı geçen HER BİR MODELİN ne olduğunu, nasıl çalıştığını ve arka planındaki matematiği **tamamen bakkal, zar atma ve günlük hayat örnekleriyle** en ince ayrıntısına kadar inceleyelim.
""")

# CHAPTER 2
append_to_md("""
## BÖLÜM 2: K-En Yakın Komşu (KNN) Algoritması

Makalelerde sıkça karşılaştırılan en ilkel ama en etkili modellerden biri **KNN (K-Nearest Neighbors)** algoritmasıdır.

**Mantığı (Bana Arkadaşını Söyle):**
Yeni bir müşteri geldi. Acaba bu müşteri bizi terk edecek mi (Churn) yoksa kalacak mı (Sadık)? 
KNN algoritması hiçbir denklem çözmez, hiçbir zar atmaz. Sadece şunu yapar: Bu yeni müşteriyi alır ve devasa veri tabanındaki diğer müşterilerin arasına (bir haritaya) koyar. Sonra **K** harfi ile belirtilen sayıda en yakın komşusuna bakar. 
Eğer K=5 seçtiysek, makine bu yeni müşterinin haritadaki en yakın 5 komşusuna (yani harcama alışkanlıkları, yaşı ve faturası bu müşteriye en çok benzeyen 5 kişiye) bakar.
- Eğer o 5 komşunun 4'ü geçmişte bizi terk etmişse (Churn), makine der ki: *"Bana arkadaşını söyle sana kim olduğunu söyleyeyim. Senin en çok benzediğin 5 adamın 4'ü gitmiş. Demek ki sen de gideceksin!"*

**Zayıflığı:** Veri tabanınızda 1 milyon müşteri varsa, yeni gelen adamı her seferinde 1 milyon kişiyle tek tek karşılaştırıp mesafesini ölçmek zorundadır. Bu yüzden çok yavaştır ve devasa şirketlerde (Telekom) tıkanır.
""")

# CHAPTER 3
append_to_md("""
## BÖLÜM 3: Naive Bayes (Olasılıksal Sınıflandırma)

Makalelerde kullanılan bir diğer model **Naive Bayes**'tir. Adındaki "Naive" (Saf/Gülünç derecede basit) kelimesi, bu algoritmanın dünyadaki her şeyin birbirinden bağımsız olduğunu sanmasından gelir.

**Mantığı (Dedektiflik):**
Siz bir dedektifsiniz. Olay yerinde 3 ipucu var: Sigara izmariti, kırmızı ruj ve 44 numara ayak izi.
Siz bu 3 ipucunu kullanarak katilin "Erkek" mi yoksa "Kadın" mı olma olasılığını hesaplıyorsunuz.
Naive Bayes, her ipucunu TEK TEK hesaplar:
- Sigara izmariti erkeklerde %60, kadınlarda %40 görülür.
- Kırmızı ruj kadınlarda %99, erkeklerde %1 görülür.
- 44 numara ayak izi erkeklerde %95, kadınlarda %5 görülür.

Model bu olasılıkları (Bayes teoremiyle) birbiriyle çarpar ve sonuca ulaşır: "Katil büyük ihtimalle Ruj süren ama 44 numara ayakkabı giyen bir erkek!"
Telekom şirketlerinde de durum aynıdır. Müşterinin faturası (ipucu 1), sözleşme süresi (ipucu 2) ve şikayet sayısı (ipucu 3) alınır. Naive Bayes bunları birbiriyle çarparak "Terk Etme Olasılığını" bulur. 
**Zayıflığı:** Adı üstünde "Saf"tır. Özelliklerin birbirini etkilediğini anlamaz. Kırmızı ruj ile 44 numara ayak izinin aynı anda bulunmasının ne kadar mantıksız olduğunu kavrayamaz, sadece olasılıkları dümdüz çarpar.
""")

# CHAPTER 4
append_to_md("""
## BÖLÜM 4: Karar Ağaçları (Decision Trees)

Makalelerde her zaman referans olarak alınan, şirket CEO'larının en sevdiği modeldir.

**Mantığı (Bakkalın Soruları):**
Bir müşterinin churn olup olmayacağına tıpkı bir "Evet/Hayır" oyunu oynar gibi karar verir.
Makine en tepeye (Kök / Root) en kritik soruyu koyar:
- **Soru 1:** "Bu müşterinin kontratı AYLIK mı, yoksa YILLIK mı?"
  - YILLIK İSE -> Güvenli Kutu.
  - AYLIK İSE -> Alt dallara in.
- **Soru 2:** "İnternet bağlantı tipi DSL mi Fiber mi?"
  - FİBER İSE -> İnternet hızlıdır, memnundur, Güvenli Kutu.
  - DSL İSE -> Alt dallara in.
- **Soru 3:** "Son 1 ayda Müşteri Hizmetlerini aradı mı?"
  - EVET İSE -> Tehlike Kutusu! Bu adam kesin terk edecek!

Bu model neden mükemmeldir? Çünkü bir banka müdürü "Bu adam neden riskli?" diye sorduğunda, model ona ağacın dallarını göstererek, *"Aylık kontratı var, interneti yavaş (DSL) ve son 1 ayda şikayet kaydı açmış"* diyerek sebebi mükemmel bir dille açıklar (Açıklanabilirlik - Interpretability).
**Zayıflığı:** Ağaç çok büyürse veriyi ezberler (Overfitting). Bir istisnayı bile kural sanıp dalları saçma sapan uzatabilir.
""")

# CHAPTER 5
append_to_md("""
## BÖLÜM 5: Rastgele Orman (Random Forest)

Karar Ağacının ezberleme (Overfitting) sorununu çözen, makalelerde hep ilk 2'ye giren muazzam bir algoritmadır.

**Mantığı (Bin Doktorluk Demokrasi Heyeti):**
Karar ağacındaki "Tek Bir Ağaç", tek bir doktordur. Bazen hastaya (müşteriye) yanlış teşhis koyabilir.
Makine Öğrenmesi mühendisleri der ki: "Neden 1 ağaca güvenelim? Orman kuralım!"
Sistem, veri setini rastgele binlerce parçaya böler ve tam 1.000 farklı küçük Karar Ağacı oluşturur. Her ağaca verinin sadece küçük bir kısmını gösterir (Örneğin bir ağaç sadece müşterinin faturasına bakar, diğeri sadece cinsiyetine bakar).
Sonra yeni bir müşteri geldiğinde, bu 1.000 ağacın hepsi aynı anda OY KULLANIR.
- 850 Ağaç: "Bu müşteri BİZİ TERK EDECEK" oyu verir.
- 150 Ağaç: "Bu müşteri BİZDE KALACAK" oyu verir.
Çoğunluk kazanır! (Demokrasi / Ensemble Learning). 
Birkaç ağaç hata yapsa bile, geri kalan 999 ağaç o hatayı oylamayla düzeltir. Bu yüzden Random Forest, churn tahmininde inanılmaz derecede isabetlidir.
""")

# CHAPTER 6
append_to_md("""
## BÖLÜM 6: Destek Vektör Makineleri (SVM) - O Büyük Efsane

Kullanıcıların en çok merak ettiği, Vafeiadis vd. (2015) makalesinde **doğruluk oranını %96.85'e çıkaran** ve tüm algoritmaları yok eden o efsanevi model: **SVM (Support Vector Machines).**

**Mantığı (Çelikten Bir Duvar Örmek):**
SVM, karar ağaçları gibi soru sormaz. KNN gibi komşulara bakmaz. SVM, veri noktalarının arasına jilet gibi düz bir "Sınır Çizgisi" (Hyperplane) çeker.
Bir masanın üzerinde 50 tane Mavi Misket (Sadık Müşteri) ve 50 tane Kırmızı Misket (Terk Eden Müşteri) olduğunu hayal edin. 
SVM'in amacı, masaya elindeki cetveli (çizgiyi) öyle bir koymaktır ki, kırmızılar tam bir tarafta, maviler tam bir tarafta kalsın. Üstelik bu cetveli koyarken, en uçtaki (sınıra en yakın) kırmızı ve mavi misketlere (Bunlara 'Destek Vektörü - Support Vector' denir) en uzak olacak şekilde en geniş, en güvenli yoldan geçirir.

### 6.1. Ya Misketler İç İçe Geçmişse? (Kernel Trick / Boyut Bükme)
Eğer masadaki kırmızı ve mavi misketler iç içe geçmişse, oraya düz bir cetvel koyamazsınız! İki grubu birbirinden düz bir çizgiyle ayıramazsınız. 
İşte SVM'in gerçek sihri burada başlar. Eğer veriler 2 boyutta ayrılamıyorsa, SVM **"Kernel Trick" (Çekirdek Hilesi)** denilen dahiyane bir matematik kullanır.

**SVM-RBF (Radial Basis Function) ve SVM-POLY (Polinom):**
Makalede tam da bunlar test edilmiştir. 
Cetvelle ayıramadığınız o iç içe geçmiş misketlerin bulunduğu masaya, **alttan çok sert bir yumruk attığınızı** hayal edin! 
Misketlerin hepsi havaya zıplar (Veri 2 boyuttan, 3 boyuta, uzaya fırlatılır). 
Misketler havadayken, SVM aralarından düz bir tepsi geçirir ve havada onları böler! Sonra yerçekimiyle misketler masaya geri düştüğünde, o dümdüz tepsi masada sanki yuvarlak, kıvrımlı, harika bir sınır çizgisi gibi görünür.

Makalede araştırmacılar **SVM-POLY (Teta=1, p=4)** yani Polinomsal Çekirdek kullanarak, müşteri verisini 4. boyuta fırlatmışlar ve sadık müşterilerle churn olanları o boşlukta devasa bir kesinlikle ikiye bölmüşlerdir.
""")

# CHAPTER 7
append_to_md("""
## BÖLÜM 7: AdaBoost ve XGBoost (Boosting / Heyecan Verici Ordu)

Makalenin (Vafeiadis 2015) can alıcı noktasına geldik. SVM kendi başına %92 doğruluk verirken, yazarlar bunu **AdaBoost** ile birleştirmiş ve oranı **%96.85'e, F-Ölçütünü (Başarıyı) %84.57'ye** fırlatmışlardır. Peki nedir bu Boosting?

**Mantığı (Hatalardan Ders Alan Zayıf Ordu):**
Random Forest (Rastgele Orman) bin tane ağacın aynı anda oy kullanmasıydı.
**AdaBoost (Adaptive Boosting)** ise ağaçların "sırayla" çalışmasıdır.

1. Sistem, çok zayıf, aptal bir algoritma (örneğin sadece 1 soruluk bir Karar Ağacı) yaratır ve müşterileri tahmin etmesini ister.
2. Bu zayıf algoritma 100 müşteriden 70'ini doğru, 30'unu yanlış tahmin eder.
3. **İşte Sihir Burada:** AdaBoost, o YANLIŞ tahmin edilen 30 müşterinin ağırlığını (kırmızı kalemle altını çizerek) devasa şekilde artırır. 
4. İkinci zayıf ağacı yaratır ve ona der ki: "Öncekilerin doğru bildiklerini boşver, senin tek görevin şu kırmızıyla çizilmiş 30 zor müşteriyi doğru bilmek!"
5. İkinci ağaç o 30 kişinin 20'sini doğru bilir, 10'unda yine hata yapar. 
6. Sistem o 10 zor müşterinin ağırlığını daha da artırır ve üçüncü ağaca verir.

Böyle böyle yüzlerce ağaç art arda dizilir. Her yeni model, bir önceki modelin yapamadığı "zor" müşterilere odaklanır (Hatalardan ders alır). Sonunda bu zayıf modeller ordusu birleştiğinde, dünyanın en güçlü tahmin makinesine (XGBoost / AdaBoost) dönüşür. 
Makalede yazarlar, bu hatalardan ders alma (Boosting) mekanizmasını **SVM** ile birleştirdiklerinde, Telekom dünyasındaki churn problemini adeta paramparça ederek çözmüşlerdir.
""")

# CHAPTER 8
append_to_md("""
## BÖLÜM 8: Yapay Sinir Ağları (ANN - Artificial Neural Networks)

Makalelerde son olarak insanın bizzat beynini taklit eden ANN'den bahsedilir.

**Mantığı (Beyin Hücreleri ve Kara Kutu):**
İnsan beyninde milyonlarca nöron (sinir hücresi) vardır ve bunlar birbirine elektrik sinyalleriyle bağlıdır.
Yapay Sinir Ağı (ANN) da aynıdır. 
- Müşterinin faturası, yaşı, sözleşmesi ağın en başından (Girdi Katmanı / Input Layer) elektrik sinyali olarak verilir.
- İçeride "Gizli Katmanlar" (Hidden Layers) denilen nöronlar vardır. Fatura yüksekse bir nöron ateşlenir, yaş gençse başka bir nöron ateşlenir.
- Bu sinyaller katmanlar arasında ağırlıklarla (weights) çarpıla çarpıla sona ulaşır (Çıktı Katmanı / Output Layer). Ve makine son sözü söyler: "CHURN!"

**Zayıflığı (Kara Kutu Problemi):**
Makaleler ANN'yi kullanır ama yöneticiler ANN'den nefret eder. Neden mi?
Çünkü ANN bir **Kara Kutu (Black Box)**'dur. Karar ağacı size "müşteri DSL kullanıyor diye gidiyor" açıklamasını yapabilirken; ANN size sadece "Bu adam gidecek" der. Neden diye sorarsanız "İçerideki 450. nöronun aktivasyon fonksiyonu ateşlendiği için" gibi hiçbir işinize yaramayacak matematiksel bir açıklama yapar. Bu yüzden şirketlerde churn engelleme aksiyonu alınacaksa, her zaman açıklanabilir modeller (Ağaçlar) Neural Network'lere tercih edilir.
""")

# CHAPTER 9
append_to_md("""
## BÖLÜM 9: Sentetik Veri (SMOTE) ve Modelin Dengesizlikle İmtihanı

Praveen Lalwani ve arkadaşlarının (2021) makalesinde, tüm bu sihirli algoritmaların tek bir damla veri hatasıyla nasıl çökeceği ve bunun nasıl çözüldüğü anlatılır.

**Problem (Dengesiz Veri - Imbalanced Data):**
Gerçek hayatta müşterilerin çoğu sizi terk etmez. Bir veri setinde 10.000 müşteri varsa, 9.000'i sadıktır, sadece 1.000'i churn olmuştur.
Eğer bu veriyi SVM'e veya Random Forest'a olduğu gibi verirseniz, makine tembellik eder. Der ki: *"Zaten herkes kalıyor. Ben algoritma falan kurmayayım, herkese 'KALACAK' diye tahmin yapayım. 10.000 kişide 9.000 doğru bilirim, Başarı oranım (Accuracy) %90 olur!"*
Makine harika bir not aldığını sanır ama şirket için sıfır işe yaramaktadır, çünkü makine "kaçacak olan o kritik 1.000 kişiyi" tamamen göz ardı etmiştir.

**Çözüm (SMOTE - Sentetik Azınlık Üretimi):**
İşte veri bilimciler algoritmaları bu tembellikten kurtarmak için **SMOTE (Synthetic Minority Over-sampling Technique)** kullanırlar.
Sistem, o kaçan 1.000 kötü müşteriye bakar. Onların DNA'sını (kredi skorunu, fatura ödemelerini) kopyalar ve bilgisayar ortamında tamamen **sahte (sentetik) 8.000 tane daha kötü müşteri klonlar!**
Artık terazinin iki tarafı eşittir: 9.000 gerçek sadık müşteri ve 9.000 (1.000 gerçek + 8.000 klon) terk eden müşteri.
Makine artık bu denge karşısında tembellik yapamaz, kötü müşterilerin özelliklerini mecburen "öğrenmek" zorunda kalır. Ve başarı oranı gerçek anlamda yükselir.
""")

# CHAPTER 10
append_to_md("""
## BÖLÜM 10: ASOS.com ve "Embedding" (Kıyafetleri Vektörlere Çevirmek)

Klasik makine öğrenmesini ve Telekom'u aşıp, e-ticaret devi ASOS.com'un Müşteri Yaşam Boyu Değerini (CLV) nasıl bulduğuna gelelim. ASOS 85.000 ürünü olan dev bir şirkettir. Ve modellerini sadece "Müşteri ne kadar harcadı?" sorusuna değil, **"Müşteri ne TARZ harcadı?"** sorusuna göre kurarlar.

**Word2Vec'ten Ürün Uzayına:**
Bilgisayar "Deri Ceket"in veya "Hasır Şapka"nın ne olduğunu bilmez. ASOS veri bilimcileri, tıpkı cümleleri kelimelerine ayıran sistemler gibi, alışveriş sepetlerini inceler. 
Müşteri hep Siyah Kot ile Deri Ceket'i aynı sepete atıyorsa, bilgisayar bu iki kıyafeti 3 Boyutlu devasa bir uzayda birbirine çok yakın bir yere konumlandırır. (Buna **Embedding** denir). Hasır şapkayı ise uzayın öbür ucuna koyar.

**Müşterinin Uzaydaki Yeri:**
Sonra algoritma "Müşteriyi" bu uzayın içine fırlatır! Müşteri uzayda hangi kıyafetlerin yanına düşerse, onun profili (iade yapma ihtimali, sadakati, tarzı) o kıyafetlerin karakterine bürünür.
Random Forest modeli, müşterinin harcadığı paraya değil, uzaydaki bu koordinatlarına (Embedding Vektörlerine) bakarak CLV tahmini yapar. Böylece Asos, sadece "Ne kadarlık aldı?" değil, "Ne tür bir ruha sahip ve bu ruh bize gelecekte ne kazandırır?" sorusunu cevaplar.
""")

# CHAPTER 11
append_to_md("""
## BÖLÜM 11: Sonuç ve En Büyük Çıkarımlar (The Grand Finale)

Tüm makine öğrenmesi modellerini, Karar Ağaçlarından SVM'e, Naive Bayes'ten XGBoost'a kadar inceledik. Bir yöneticinin veya veri bilimcinin bu makaleler deryasından çıkarması gereken altın kurallar şunlardır:

1. **Hiçbir Algoritma Sihirli Değildir:** Eğer veriniz kötüyse, eksikse veya SMOTE gibi araçlarla dengelenmemişse, dünyanın en gelişmiş Derin Öğrenme modeli bile çuvallar (Garbage in, Garbage out).
2. **Kara Kutu vs. Açıklanabilirlik Paradoksu:** SVM ve Neural Networks size en yüksek başarıyı (%96.85) verebilir. Ancak genel müdür "Ahmet neden gidiyor?" dediğinde bu modeller size bir şey söyleyemez. Neden sorusunun cevabını istiyorsanız başarısı daha düşük ama "konuşabilen" modelleri (Karar Ağaçları) seçmek zorundasınız.
3. **Malthouse'un Uyarısı (Gelecek Körlüğü):** Bir müşterinin geçmişteki "en iyi müşteri" olması, gelecekte de öyle olacağı anlamına gelmez. Makine öğrenmesi sadece bugünün röntgenini çeker. İnsan hayatı değişkendir (evlilik, taşınma, işsizlik). Bu kaosu tamamen %100 doğrulukla tahmin edebilecek bir yapay zeka yoktur ve asla olmayacaktır. Tüm bu algoritmalar geleceği bilmek için değil, *riski minimize etmek* için vardır.
""")

print("Markdown content written.")

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
            --primary-dark: #0f172a; /* Slate 900 */
            --primary: #1e293b; /* Slate 800 */
            --accent: #2563eb; /* Royal Blue */
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

        /* COVER PAGE STYLING */
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

        /* CONTENT STYLING */
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
            <div class="cover-subtitle">Karar Ağaçlarından SVM'e, KNN'den Boosting'e Bütün Modellerin "Bakkal Mantığıyla" Adım Adım İspatı</div>
            <div class="cover-author">TAM KAPSAMLI LİTERATÜR (TÜM MODELLER)</div>
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

print("Ansiklopedik ML PDF (ALL MODELS) created successfully!")
