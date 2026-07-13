import os
import markdown
from playwright.sync_api import sync_playwright

md_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.md'
html_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.html'
pdf_file = r'c:\Users\emink\Desktop\zorunlu staj\başta verilen makale\Ansiklopedik_Makine_Ogrenmesi_Rehberi.pdf'

# Clear the file first
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# Makine Öğrenmesi ve CLV: A'dan Z'ye Basit ve Detaylı Rehber\n\n")

def append_to_md(content):
    with open(md_file, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")

# CHAPTER 1
append_to_md("""
## BÖLÜM 1: Churn'ün Anatomisi - Müşteri Bizi Neden Terk Eder?

Önceki rehberlerde olasılık modelleriyle "Müşteri öldü mü?" sorusunu sormuştuk. Ancak bu klasördeki makaleler (özellikle Telekomünikasyon analizleri) işin sosyolojisine iner: **Müşteri NEDEN ölür?**

Makaleler Churn (Müşteri Kaybı) olayını, tıpkı hastalıkları sınıflandırır gibi iki devasa kategoriye ayırır. Bir firmayı yönetiyorsanız, kimi neden kaybettiğinizi bilmek, onu kurtarmanın ilk şartıdır.

### 1.1. Zorunlu Kayıp (Involuntary Churn)
Bu, müşterinin kendi isteğiyle değil, **şirketin zorlamasıyla** gerçekleşen ayrılıktır. 
**Bakkal Mantığıyla Örnek:** Mahalle bakkalına veresiye yazdıran bir müşteri aylarca borcunu ödemez. Bakkal Ahmet Amca bir gün sinirlenir ve "Sana artık ekmek yok, defol git!" der.
Kurumsal dünyada bu şudur: Müşteri faturasını ödemez, sahte evrak kullanır veya dolandırıcılık yapar. Şirket (örneğin Türk Telekom veya Vodafone), abonenin hattını tek taraflı olarak kapatır. 
*Veri Bilimciler için not:* Makine öğrenmesi modeli kurarken, borcunu ödemediği için atılan bu müşterileri veri setinden "temizlemek" zorundasınız. Çünkü sizin tahmin etmeye çalıştığınız şey "kimin faturasını ödeyemeyeceği" değil, "kimin rakip firmaya kaçacağıdır". Eğer bunları ayırmazsanız, algoritmanız çöplüğe döner.

### 1.2. Gönüllü Kayıp (Voluntary Churn)
Bu, müşterinin tamamen kendi iradesiyle bavulunu toplayıp rakip firmaya geçmesidir. Kendi içinde ikiye ayrılır:

**A. Tesadüfi (Incidental) Kayıp:**
Müşterinin firmaya hiçbir kastı veya kızgınlığı yoktur. Sadece hayat şartları değişmiştir.
**Örnek:** Müşteri İstanbul'dan Hakkari'ye taşınır. Sizin mağazanız Hakkari'de olmadığı için mecburiyetten sizi bırakır. Veya müşteri vefat eder. 
Bunu yapay zeka ile **tahmin edemezsiniz.** Hiçbir makine öğrenmesi algoritması müşterinin yarın kalp krizi geçireceğini veya tayininin çıkacağını bilemez. Bu yüzden bu gruptakiler analizlerde "gürültü" (noise) olarak kabul edilir.

**B. Bilinçli (Deliberate) Kayıp:**
İşte bütün makine öğrenmesi mühendislerinin, milyarlarca dolarlık bütçelerle çözmeye çalıştığı asıl düşman budur! 
Müşteri faturasını ödeyebilir, aynı şehirde yaşıyordur ama **kasıtlı olarak** rakip firmayı seçer. Neden? 
- **Fiyat Hassasiyeti:** Rakip banka bedava EFT sunmuştur.
- **Hizmet Kalitesi:** Müşteri hizmetlerini aramış, 30 dakika telefonda beklemiş ve çıldırmıştır.
- **Teknoloji:** Sizin internetiniz sürekli kopuyordur, rakip firma fiber optik çekmiştir.

Yapay Zeka (Karar Ağaçları, SVM, Random Forest), sadece ve sadece bu gruptaki müşterilerin ayak izlerini (şikayet kayıtları, çağrı süresi, internet kullanımı) takip ederek, "Bu adam patlamaya hazır bir bomba, yarın rakibe geçecek" uyarısı veren sistemlerdir.
""")

# CHAPTER 2
append_to_md("""
## BÖLÜM 2: Karar Ağaçları (Decision Trees) - Bakkalın Zihin Haritası

Makalelerde (özellikle IBM Watson Telco veri setinin analizinde) makine öğrenmesi yöntemleri kıyaslanırken **Decision Tree (Karar Ağacı)** hep en öne çıkar. Çünkü Karar Ağacı, insan beyninin çalışma şeklinin birebir aynısıdır. Matematiği yoktur, sadece "MANTIK" vardır.

**Mala Anlatır Gibi "Karar Ağacı" Nedir?**
Bakkal Ahmet Amca'nın zihninde bir "Borç Verilir mi?" haritası vardır. Biri veresiye istediğinde Ahmet Amca şu sırayla sorular sorar:

1. **Soru 1:** Bu adam bizim mahalleden mi?
   - **HAYIR İSE:** Yabancıya borç verilmez! (Karar: VERME).
   - **EVET İSE:** Bir sonraki soruya geç.
2. **Soru 2:** Geçen aydan borcu var mı?
   - **EVET İSE:** Borçluya borç verilmez! (Karar: VERME).
   - **HAYIR İSE:** Bir sonraki soruya geç.
3. **Soru 3:** Maaşlı bir işi var mı?
   - **HAYIR İSE:** Ödeyemez. (Karar: VERME).
   - **EVET İSE:** (Karar: BORÇ VER).

İşte Karar Ağacı tam olarak budur! Veriyi alır, en tepeden (Kök - Root) başlar ve müşterileri Evet/Hayır sorularıyla dallara ayırır. 

**Telekomünikasyon Şirketinde Karar Ağacı Nasıl Çalışır?**
Yapay zeka binlerce müşterinin verisini inceler ve en önemli "bölücü" soruyu en tepeye koyar:
- **Kök Soru:** "Müşterinin kontratı AYLIK mı, yoksa 2 YILLIK mı?"
Eğer müşteri 2 yıllık kontrat yapmışsa, ağaç onu hemen "GÜVENLİ (Churn olmaz)" kutusuna atar. (Çünkü cayma bedeli yüksektir).
Eğer müşteri AYLIK kontrattaysa, ağaç bir soru daha sorar:
- "İnternet türü Fiber mi, DSL mi?"
Eğer Fiber ise, hızdan memnundur, "GÜVENLİ" kutusuna atar.
Eğer DSL ise ve aylık kontratı varsa, ağaç onu "TEHLİKELİ (Churn olacak!)" kutusuna koyar.

Karar ağaçlarının yöneticiler tarafından bu kadar çok sevilmesinin tek nedeni, modelin **"Açıklanabilir" (Interpretable)** olmasıdır. Yönetici "Bu adam neden bizi terk edecek?" diye sorduğunda, Karar Ağacı ona sebebi madde madde (DSL kullanıyor, aylık ödüyor, teknik servisi çok aramış) açıklar.
""")

# CHAPTER 3
append_to_md("""
## BÖLÜM 3: Rastgele Orman ve Destek Vektör Makineleri (Heyet Kararı)

Karar Ağaçları çok anlaşılırdır ama bir sorunları vardır: Bazen veriyi ezberlerler (Overfitting). Ahmet Amca sadece kendi mahallesindeki 5 kişiye bakarak bir kural koyarsa, yan mahalleden gelen düzgün bir müşteriye haksızlık edebilir.
Bu sorunu çözmek için makalelerde iki devasa algoritma daha kullanılır: Random Forest (Rastgele Orman) ve SVM (Destek Vektör Makineleri).

### 3.1. Random Forest (Rastgele Orman): Tek Akıl Yerine Ortak Akıl
"Random Forest", adından da anlaşılacağı gibi tek bir Karar Ağacı değil, binlerce karar ağacından oluşan bir ormandır.

**Mala Anlatır Gibi Örneği:**
Diyelim ki hastasınız ve ameliyat olup olmayacağınıza karar vereceksiniz.
Eğer sadece bir doktora giderseniz (Karar Ağacı), doktor kendi tecrübesine göre "Ameliyat ol" diyebilir. Ama o doktor belki yanılıyordur.
Eğer **1.000 farklı doktordan oluşan bir heyet** kurarsanız ve her bir doktora sizin tahlillerinizin sadece bir kısmını gösterip, hepsinden oy vermelerini isterseniz ne olur?
Doktorların 800'ü "Ameliyat ol", 200'ü "Olma" derse, çoğunluğun oyu (Demokrasi) kazanır.
İşte Random Forest budur. Veri setini binlerce parçaya böler, 1.000 farklı "zayıf" karar ağacı oluşturur ve onlara oy kullandırtır. Bir ağaç hata yapsa bile diğer 999 ağaç o hatayı düzeltir. Telekomünikasyon churn tahmininde genellikle **en yüksek başarı oranını (%85-90)** hep Random Forest verir.

### 3.2. Destek Vektör Makineleri (SVM): Duvar Örmek
SVM'in çalışma mantığı oylama değil, "sınır çizmektir". 
Masanın üzerinde kırmızı ve mavi renkte 100 tane misket olduğunu düşünün. Misketlerin bazıları iç içe geçmiş.
Amacınız, masaya dümdüz bir cetvel (çizgi) koyarak kırmızıları bir tarafta, mavileri diğer tarafta bırakmak. 
Eğer masanın üzerinde bu çizgiyi (Linear ayrım) çekemiyorsanız, SVM çok sihirli bir matematik numarası yapar (Kernel Trick): Masaya alttan vurur! Misketler havaya zıplar (veri 3 boyutlu hale gelir) ve misketler havadayken aralarından düz bir tepsi (Hyperplane) geçirerek onları ayırır.
SVM, müşterileri "Sadıklar" ve "Terk Edecekler" olarak ayırmak için veriyi matematiksel bir uzaya fırlatıp aralarına çelikten bir duvar ören son derece katı ve güçlü bir algoritmadır.
""")

# CHAPTER 4
append_to_md("""
## BÖLÜM 4: 6 Aşamalı Churn Tahmin Fabrikası (Telco Örneği)

Makalelerde (Praveen Lalwani ve ark.) "Biz bu makine öğrenmesini nasıl kuruyoruz?" sorusuna bir sistem mimarisi (fabrika boru hattı) ile cevap verilir. Makineye veriyi ham haliyle atamazsınız, makine anında kusar. Bu iş 6 aşamalı bir rafineri işlemidir:

1. **Veri Seçimi (Data Identification):** Neyi inceleyeceğiz? IBM Watson'ın Telekom verisi (Müşterinin yaşı, cinsiyeti, aylık faturası, sözleşme türü, teknik servisi kaç kez aradığı).
2. **Veri Ön İşleme (Data Preprocessing):** Sizin veritabanınızda boş hücreler vardır ("Maaşı" kısmı girilmemiş). Cinsiyet "Erkek/Kadın" olarak yazılıdır ama bilgisayar yazıyı okuyamaz. Bu aşamada "Boş" hücreler ortalamayla doldurulur. "Erkek" yerine "1", "Kadın" yerine "0" yazılır. Veri makinenin yiyebileceği rakamlara dönüştürülür.
3. **Özellik Seçimi (Feature Selection):** Müşterinin ayakkabı numarası churn'ü etkiler mi? Etkilemez. O zaman bu gereksiz bilgiyi veriden atmalısınız ki makinenin kafası karışmasın. Yalnızca en güçlü sinyaller (Sözleşme tipi, ödeme yöntemi, fatura tutarı) modelin içine alınır.
4. **Sentetik Veri Üretimi (SMOTE):** Bu çok kritik bir adımdır! Sizin 10.000 müşteriniz var. Bunların 9.000'i sadık, sadece 1.000'i churn (terk eden). Veri **dengesizdir (imbalanced).** Makine bu veriyi okursa der ki: "Zaten herkes kalıyor, ben tahminde bulunmayayım, herkese 'kalacak' diyeyim, %90 başarılı olurum."
Bunu engellemek için veri bilimciler SMOTE denilen bir yöntemle, o 1.000 kötü müşterinin verilerini kopyalayıp sahte (sentetik) kötü müşteriler üretirler ve teraziyi 5.000 İyi / 5.000 Kötü olarak dengelerler. Makine artık iyiyi de kötüyü de eşit ciddiyetle öğrenmek zorunda kalır.
5. **Modelin Eğitilmesi (Training):** Veri, Decision Tree, Random Forest veya SVM'e verilir. Makine geçmiş verilere bakarak kuralları bulur.
6. **Değerlendirme (Evaluation):** Modelin başarısı test edilir. Burada sadece "Accuracy" (Doğruluk) oranına bakılmaz. Çünkü 99 kere doğru bilip, 1 kere en değerli müşterinin kaçışını gözden kaçırırsa şirket batar. O yüzden Recall (Gözden kaçırmama yeteneği) ve Precision (Attığını vurma yeteneği) ölçülür.
""")

# CHAPTER 5
append_to_md("""
## BÖLÜM 5: Müşteri Yaşam Boyu Değeri Gerçekten Tahmin Edilebilir Mi?

Malthouse & Blattberg (2005) makalesi veri bilimcilere soğuk bir duş aldırır. 
Şirketler CLV (Customer Lifetime Value) modellerini kurup, "Bu müşteri bana gelecek 5 yılda tam 12.500 TL kazandıracak" diye devasa excel tabloları hazırlarlar. Blattberg bu makalesinde şu tokat gibi soruyu sorar: **"Bunu yapabileceğinize gerçekten inanıyor musunuz?"**

**Geleceği Görme İllüzyonu**
Yazarlar, şirketlerin gelecekteki "en karlı" müşterileri önceden tespit edip tüm parayı (CRM bütçesini) onlara harcaması gerektiği fikrini test ederler. Sonuç şok edicidir:
Model geçmişe bakarak çok iyi çalışır ama **geleceği tahmin etmede (R-Kare - R^2 doğruluk oranında) feci şekilde çuvallar.**
- Sizin bugün "en iyi müşteri (Top %20)" olarak etiketlediğiniz adam, yarın işsiz kalır ve 5 kuruş harcamaz.
- Sizin "buna reklam atmaya değmez" deyip çöpe attığınız bir öğrenci, 1 yıl sonra mezun olur, yüksek maaşlı işe girer ve en sadık, en paralı müşteriniz olur.

**Ders:** Modeller, eldeki veriye bakarak bir "eğilim" belirleyebilir ama insan hayatının kaotik doğasını (evlilik, boşanma, işe girme, kaza geçirme, hevesin geçmesi) asla tam olarak tahmin edemez. Olasılık modelleri bir kristal küre değildir, sadece riski yönetme araçlarıdır. Bütün pazarlama bütçenizi "algoritmanın en iyi 10 müşterisi" listesine basarsanız iflas edersiniz.
""")

# CHAPTER 6
append_to_md("""
## BÖLÜM 6: Derin Öğrenme ve "Embedding" (ASOS.com Örneği)

Klasik makine öğrenmesini (Karar ağaçları) geçtik, şimdi 2017 yılına, yapay zekanın en derin uçlarına, ASOS.com (Global Giyim Firması) vaka analizine geliyoruz.
Asos.com'un 12 milyon müşterisi ve 85.000 farklı kıyafeti var. Klasik modeller, müşteriye "Ahmet toplam 500 TL harcadı" diye bakar.
Ancak Asos'un kurduğu "Neural Embeddings" (Yapay Sinir Ağı Gömme İşlemi) olaya tamamen başka bir boyuttan bakar: **İnsanın ruhunu, tarzını ve hislerini matematiksel vektörlere çevirmek.**

### 6.1. Kelime Vektörlerinden (Word2Vec) Kıyafet Vektörlerine
Google zamanında "Word2Vec" diye bir şey icat etmişti. Bu sistem, kelimelerin anlamlarını birbirine olan yakınlıklarına göre sayılara (vektörlere) çevirir. 
Örneğin algoritma yüzbinlerce kitap okur ve şunu fark eder: "Kral" kelimesi ile "Erkek" kelimesi genelde yan yanadır. "Kraliçe" ile "Kadın" yan yanadır. O halde bilgisayar şu denklemi kurar:
**[Kral] - [Erkek] + [Kadın] = [Kraliçe]**

ASOS bunu kıyafetlere uyarlamıştır! Müşterilerin alışveriş sepetlerini bir "cümle", içindeki kıyafetleri de "kelime" olarak kabul ederler.
Ahmet'in Sepeti: `[Siyah Dar Kot] + [Deri Ceket] + [Siyah Bot]`
Ayşe'nin Sepeti: `[Çiçekli Yazlık Elbise] + [Hasır Şapka] + [Sandalet]`

Asos'un Yapay Sinir Ağı, ürünleri birbirine olan ilişkisine göre 3 boyutlu bir uzaya yerleştirir (Embedding). Siyah bot ile Deri ceket uzayda yan yanadır. Çiçekli elbise ile Hasır şapka yan yanadır.
Daha sonra müşteri "Ahmet" de bu uzaya yerleştirilir! Ahmet uzayda deri ceketin hemen yanında durur.

### 6.2. Neden Bu Kadar Etkili?
ASOS bu sayede şunu fark etmiştir: "Müşterinin gelecekteki değerini (CLV) tahmin etmenin en iyi yolu, onun ne kadar para harcadığına değil, **UZAYDA HANGİ GRUBA (Tarza) YAKIN OLDUĞUNA** bakmaktır."
Çünkü "Deri Ceket ve Siyah Bot" giyen (Rock tarzı) genç bir müşterinin iade oranı, "Düğünlük Abiye" alan bir teyzenin iade oranından tamamen farklıdır. (Kıyafet e-ticaretinde en büyük sorun bedeni uymayan kıyafetlerin sürekli iade edilerek şirketi zarara sokmasıdır).
ASOS, müşterinin sadece sepetindeki "ürün kodlarına" bakarak onun tarzını, iade yapma ihtimalini ve firmaya olan sadakatini muazzam bir kesinlikle (Random Forest algoritmasını bu embedding vektörleriyle besleyerek) tahmin etmeyi başarmıştır. Bu, perakendenin geleceğidir.
""")

# CHAPTER 7
append_to_md("""
## BÖLÜM 7: Sonuç ve Çıkarımlar

Bu klasördeki makaleler bize veri biliminin şu kuralını öğretir: **Her araba her yolda sürülmez.**

1. Eğer elinizde "Ahmet neden iptal etti?" sorusunun cevabını yöneticinize (insanlara) açıklamanız gereken bir sunum varsa, ASOS.com'un uzay vektörlerini (Deep Learning) kullanamazsınız. O kara kutudur, yönetici bir şey anlamaz. Anlatılabilecek tek şey **Karar Ağaçlarıdır (Decision Trees).** 
2. Eğer "Ben nedenini umursamıyorum, yeter ki kimin iptal edeceğini en yüksek isabetle bileyim" diyorsanız, binlerce doktorlu heyet olan **Random Forest** kullanmalısınız.
3. Eğer elinizdeki veri çok dengesizse (sadece 10 iptal, 10.000 sadık müşteri varsa), algoritmayı kurmadan önce mutlaka **SMOTE** ile sahte kötü müşteriler üretip veriyi teraziye sokmalısınız. Yoksa makine hiçbir şey öğrenemez.
4. Malthouse'un uyarısını asla unutmayın: Olasılık ve makine öğrenmesi modelleri kristallere bakıp geleceği gösteren büyücüler değildir. İnsan hayatı değişkendir. Siz en iyi müşterinizi el üstünde tutarken, asıl servet "yarın mezun olup işe girecek olan" o kenardaki öğrencinin cebindedir. Modeller size sadece bugünün fotoğrafını çeker, geleceğe körü körüne inanmanızı istemez.
""")

print("Markdown content written.")

# Convert to HTML
with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

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
            --accent: #0ea5e9; /* Sky Blue for Tech Feel */
            --accent-light: #e0f2fe;
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
            font-size: 11pt;
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
            background: #f8fafc;
            position: relative;
        }
        
        .cover-border {
            position: absolute;
            top: 30px;
            left: 30px;
            right: 30px;
            bottom: 30px;
            border: 4px solid var(--primary-dark);
            z-index: 1;
        }

        .cover-inner {
            position: absolute;
            top: 40px;
            left: 40px;
            right: 40px;
            bottom: 40px;
            border: 1px dashed var(--accent);
            z-index: 1;
        }

        .cover-content {
            z-index: 2;
            padding: 50px;
            background: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            max-width: 80%;
        }

        .cover-title {
            font-size: 34pt;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 30px;
            color: var(--primary-dark);
        }
        
        .cover-divider {
            height: 6px;
            width: 150px;
            background-color: var(--accent);
            margin: 0 auto 40px auto;
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
            margin-top: 60px;
            font-family: 'Open Sans', sans-serif;
            font-size: 14pt;
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
            font-size: 15pt;
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
            <div class="cover-subtitle">Karar Ağaçları, Neural Embedding ve Telekom Modellerinin "Bakkal Mantığıyla" Adım Adım İspatı</div>
            <div class="cover-author">BAŞTA VERİLEN MAKALELER / DEV REHBER</div>
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

print("Ansiklopedik ML PDF created successfully!")
