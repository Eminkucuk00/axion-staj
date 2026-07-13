# Makine Öğrenmesi & CLV Dev Ansiklopedisi: Uzun ve Tam Kapsamlı Rehber


## BÖLÜM 1: Makalelerin Özü ve Müşteri Kaybının Sosyolojisi

Bu ansiklopedi, makine öğrenmesinin en karmaşık algoritmalarını, hiçbir detayı atlamadan, hiçbir formülü es geçmeden ama tamamen "bakkal mantığıyla" size sunmak için hazırlanmıştır. Makalelerde (Vafeiadis vd. ve Lalwani vd.) dünya üzerindeki tüm temel algoritmalar adeta birbiriyle savaştırılır. Ancak bu savaşı anlamak için önce ne ile savaştığımızı, yani "Churn" (Müşteri Kaybı) canavarını çok iyi tanımamız gerekir.

### 1.1. Zorunlu Kayıp (Involuntary Churn)
Bu tür, tamamen şirketin inisiyatifiyle gerçekleşen bir ayrılıktır. Müşteri gitmek istemez, şirket müşteriyi kovar.
**Neden Kovulur?**
Diyelim ki bir telekomünikasyon operatörünüz var. Müşteriniz 3 ay boyunca faturasını ödemedi veya sahte bir kredi kartıyla sisteme kayıt oldu. Şirketinizin risk birimi bu durumu fark eder ve müşterinin hattını tek taraflı olarak iptal eder. 
**Veri Bilimi Açısından Önemi:** Eğer makine öğrenmesi algoritmaları kuruyorsanız, bu insanları veri setinizden Cımbızla ayıklamak zorundasınız. Çünkü makine öğrenmesinin amacı "Kimin faturasını ödeyemeyecek kadar fakirleştiğini" bulmak değil, "Kimin rakip operatöre kendi isteğiyle geçeceğini" tahmin etmektir. Eğer zorunlu kayıpları modelinize dahil ederseniz, makine tamamen yanlış bir profil (dolandırıcı profili) öğrenir ve asıl bulması gereken rekabet kaynaklı kaçışları gözden kaçırır.

### 1.2. Gönüllü Kayıp (Voluntary Churn)
İşte makine öğrenmesi mühendislerinin yıllarını harcadığı asıl savaş alanı burasıdır. Müşteri tamamen kendi hür iradesiyle bavulunu toplar ve rakip firmaya geçer. Ancak bu da kendi içinde ikiye ayrılır:

**A. Tesadüfi Kayıp (Incidental Churn):** Müşterinin firmaya hiçbir kastı, kızgınlığı veya şikayeti yoktur. Örneğin, İstanbul'da yerel bir internet sağlayıcısı kullanıyordur ancak tayini Kars'a çıkmıştır. Kars'ta sizin altyapınız olmadığı için mecburen rakip firmaya geçer. Veya müşteri vefat etmiştir. 
Bunu dünyadaki hiçbir yapay zeka tahmin edemez! Makine, müşterinin yarın tayininin çıkacağını bilemez. Bu yüzden modeller kurulurken bu gruptaki kayıplar "Gürültü" (Noise) olarak kabul edilir ve %100 başarı oranına ulaşmanın imkansız olmasının temel sebebi bu tesadüflerdir.

**B. Bilinçli Kayıp (Deliberate Churn):** İşte asıl düşmanımız budur! Müşterinin faturayı ödeyecek parası vardır, aynı şehirde yaşıyordur ama BİLİNÇLİ OLARAK rakibe gitmektedir. Neden?
- *Fiyat:* Rakip firma aynı interneti yarı fiyatına vermektedir.
- *Hizmet Kalitesi:* Müşteri hizmetlerini aramış, yarım saat müzik dinletilmiş ve sorunu çözülmemiştir.
- *Teknoloji:* Rakip firma fiber altyapı çekmiştir.
Makine öğrenmesi modelleri sadece ve sadece bu gruptaki insanların "ayak izlerini" (çağrı merkezi kayıtları, sözleşme süreleri, aylık fatura miktarları) okuyarak kimin bilinçli bir şekilde kaçacağını tahmin etmeye çalışır.



## BÖLÜM 2: K-En Yakın Komşu (KNN) Algoritması

Makalelerde hep temel bir referans noktası olarak kullanılan KNN (K-Nearest Neighbors), makine öğrenmesi dünyasının en ilkel ama en sezgisel algoritmalarından biridir. 

**Nasıl Çalışır? (Bana Arkadaşını Söyle):**
Elinizde devasa bir müşteri haritası olduğunu düşünün. Bu haritada sağa doğru gittikçe "Yaş", yukarı doğru çıktıkça "Aylık Fatura Tutarı" artıyor olsun. Eski müşterilerinizin hepsi bu haritada birer nokta olarak işaretlenmiş. Kırmızı noktalar sizi terk edenler (Churn), Mavi noktalar ise sadık kalanlar.

Şimdi içeri yepyeni bir müşteri girdi: Ahmet. Ahmet'in yaşını ve faturasını biliyoruz, bu yüzden onu haritaya tam koordinatlarına yerleştiriyoruz. Peki Ahmet bizi terk edecek mi?
KNN algoritması matematikle veya formüllerle uğraşmaz. Sadece Ahmet'in etrafına bir daire çizer ve **K** sayısına (Örneğin K=5 olsun) bakar. Ahmet'in haritadaki en yakın 5 komşusunu bulur. 
Bu "komşu" demek, yaşı ve fatura tutarı Ahmet'e en çok benzeyen 5 insan demektir.
Makine o 5 komşuya bakar. Eğer o 5 kişinin 4'ü kırmızı (Terk etmiş) ve 1'i mavi (Sadık) ise, KNN algoritması Ahmet için şu kararı verir: *"Bana arkadaşını söyle, sana kim olduğunu söyleyeyim. Senin profilinin birebir aynısı olan 5 kişiden 4'ü gitmiş. O zaman büyük bir ihtimalle sen de gideceksin!"*

**Neden Zayıftır?**
KNN tembel bir algoritmadır (Lazy Learning). Geçmişten genel bir "kural" çıkarmaz. Milyonlarca müşterisi olan bir Telekom şirketine yeni bir müşteri geldiğinde, sistem o yeni müşteriyi *tek tek* diğer 1 milyon müşteriyle karşılaştırıp aralarındaki mesafeyi ölçmek zorundadır. Bu işlem çok uzun sürer, bilgisayar sistemlerini kilitler ve büyük verilerde (Big Data) inanılmaz hantal kalır.



## BÖLÜM 3: Naive Bayes (Olasılıksal Dedektiflik)

Makalelerde sıkça geçen Naive Bayes, gücünü istatistiğin temeli olan "Bayes Teoremi"nden alır. Adındaki "Naive" kelimesi "Saf, Çocuksu" anlamına gelir. Neden ona "Saf" dendiğini çok detaylı bir dedektiflik hikayesiyle anlatalım.

**Dedektiflik Mantığı:**
Bir cinayet mahalli düşünün. Siz başmüfettişsiniz ve elinizde sadece 3 ipucu var:
1. Olay yerinde bir sigara izmariti var.
2. Bardakta kırmızı ruj izi var.
3. Yerde 44 numara bir ayak izi var.

Amacınız katilin "Erkek" mi yoksa "Kadın" mı olduğunu bulmaktır. Geçmiş tüm cinayet dosyalarına bakıyorsunuz ve şu istatistikleri çıkarıyorsunuz:
- Sigara izmariti bırakan katillerin %60'ı Erkek, %40'ı Kadındır.
- Ruj izi bırakan katillerin %99'u Kadın, %1'i Erkektir (Belki de erkek katil hedef şaşırtmak için ruj sürmüştür).
- 44 numara ayakkabı giyen katillerin %95'i Erkek, %5'i Kadındır.

Naive Bayes algoritması bu üç ipucunu alır ve Erkeğin Katil Olma Olasılığı ile Kadının Katil Olma Olasılığını ayrı ayrı hesaplar. Bunu yaparken bu üç oranı BİRBİRİYLE ÇARPAR.
- **Erkek Olma İhtimali Skoru:** 0.60 * 0.01 * 0.95 = 0.0057
- **Kadın Olma İhtimali Skoru:** 0.40 * 0.99 * 0.05 = 0.0198

Skorları kıyaslar ve der ki: "Kadın olma ihtimali skoru (0.0198), Erkek olma ihtimali skorundan (0.0057) daha yüksek. Katil kesinlikle KADIN!"

**Neden "Saf" Deniyor?**
Çünkü Naive Bayes algoritması dünyadaki her özelliğin **BİRBİRİNDEN TAMAMEN BAĞIMSIZ** olduğunu sanacak kadar saftır.
Düşünün; 44 numara ayakkabı giyen birinin aynı zamanda dudaklarına kırmızı ruj sürmüş olması gerçek hayatta birbirini dışlayan, çok tutarsız iki olaydır. Normal bir insan der ki: "Bu ruj kesinlikle hedef şaşırtmak için konulmuş, 44 numara ayaklı bir kadının ruj sürme ihtimali yoktur, bu kesinlikle erkek!"
Ancak Naive Bayes bu ipuçları arasındaki "ilişkiyi" asla göremez. O sadece sayılara bakar, dümdüz çarpar ve geçer.
Müşteri kaybında da faturası çok yüksek olan birinin aynı zamanda çok genç olması arasındaki ince ilişkiyi anlayamaz. Bu "saflığına" rağmen, özellikle çok fazla verinin olduğu (örneğin kelime analizi, spam e-posta filtreleme) konularda şaşırtıcı derecede hızlı ve başarılı çalışır.



## BÖLÜM 4: Lojistik Regresyon (Esnek "S" Eğrisinin İcadı)

Makine öğrenmesine geçişin en temel kapısı Lojistik Regresyon'dur. Adı "Regresyon" (gelecekteki sayısal bir değeri tahmin etme) olsa da, bu aslında "Evet/Hayır" kararı veren bir Sınıflandırma algoritmasıdır.

**Düz Çizginin Çöküşü:**
X ekseninde müşterinin firmayla geçirdiği Yıl, Y ekseninde ise Churn (0=Kalacak, 1=Gidecek) yazdığını düşünün.
Amacımız, müşterinin yıllarına bakarak onun gitme İHTİMALİNİ (Yüzdesini) bulmaktır. Eğer siz Lineer (Doğrusal) bir çizgi çekerseniz çok komik bir durum ortaya çıkar. 
Diyelim ki çizgi yukarı doğru dümdüz gidiyor. 10 yıllık bir müşteri sisteme girdiğinde çizgi grafiğin dışına taşar ve size şu cevabı verir: *"Bu müşterinin bizi terk etme ihtimali Yüzde 150'dir!"* Veya çok yeni bir müşteri için *"Terk etme ihtimali Eksi Yüzde 30'dur"* der.
İhtimal %100'den büyük veya 0'dan küçük Olamaz! İstatistikte böyle bir saçmalık kabul edilemez.

**Sigmoid Fonksiyonu (Sihirli Bükülme):**
Matematikçiler bu dümdüz ilerleyen çizgiyi almışlar ve uçlarından tutup bükmüşlerdir. Ortaya **"S" harfi şeklinde bir eğri (Sigmoid Curve)** çıkmıştır.
Bu "S" eğrisi, sonsuza kadar uzansa bile ASLA 1'i (Yani %100'ü) yukarı doğru aşamaz. Ve ASLA 0'ın (Yani %0'ın) altına inemez.
Artık makineye 20 yıllık bir müşteriyi bile sorsanız, o esnek "S" eğrisinin üzerine gelir ve size matematiksel olarak mükemmel bir oran verir: *"Terk etme olasılığı %98.5'tir"* der. Asla %100 demez, daima bir şüphe payı bırakır. 
Firmalar Lojistik Regresyonu çok severler çünkü sistem size sadece "Gidecek" demez. Bütün müşterilerinizi 0 ile 1 arasında sıralar. Böylece şirket, pazarlama bütçesini "Terk etme ihtimali en yüksek %90 olanlardan" başlayarak en risklilere harcayabilir.



## BÖLÜM 5: Karar Ağaçları ve Soru Sorma Sanatı

İşte şirket CEO'larının masasına en rahat koyabileceğiniz, tamamen "Mantık" ile çalışan Karar Ağaçları (Decision Trees).

**Bakkal Ahmet Amca'nın Zihin Haritası:**
Algoritma tıpkı deneyimli bir esnaf gibi çalışır. Gelen müşteriyi yukarıdan aşağıya süzerek ardışık sorular sorar.
*Soru 1:* "Bu müşteri AYLIK kontrata mı sahip, yoksa YILLIK kontrata mı?"
Eğer müşteri yıllık kontrata sahipse, onu hemen "GÜVENLİ (Kalacak)" kutusuna atar. Çünkü yıllık kontratı bozmanın yüksek bir cezası vardır, müşteri kolay kolay gidemez.
Eğer aylık ise, müşteri henüz cebe girmemiştir, onu alt dala gönderir ve ikinci soruyu sorar.
*Soru 2:* "Bu müşterinin kullandığı internet Fiber mi, yoksa eski nesil DSL mi?"
Eğer Fiber ise hızı iyidir, "GÜVENLİ" kutusuna atar. Eğer DSL ise, yavaştır, tehlike çanları çalar, bir alt dala daha gönderir.
*Soru 3:* "Son 3 ayda müşteri hizmetlerini teknik arıza için aradı mı?"
Eğer Evet ise, algoritma son mührü basar: *"TEHLİKE! Bu müşteri DSL kullanıyor, teknik servisle kavga etmiş ve aylık kontratı var. Yarın iptal edecek!"*

Bu algoritmanın en büyük gücü **"Açıklanabilirlik" (Interpretability)** olmasıdır. Bir model hata yapsa bile, nerede ve neden hata yaptığını satır satır okuyabilirsiniz. İnsan beyniyle aynı çalışır.

### 5.1. Ağaç İlk Soruyu Neye Göre Sorar? (Gini Index ve Information Gain)
Aklınıza şu muazzam soru gelmiş olmalı: Bilgisayar en tepedeki (Kök) soru olarak neden "Cinsiyeti nedir?" veya "Faturası kaç TL'dir?" sorusunu sormuyor da "Sözleşme tipi nedir?" sorusunu soruyor? Karar ağacı hangi sorunun en önemli soru olduğunu nasıl anlıyor?
İşte burada işin içine **Gini Safsızlığı (Impurity)** ve **Bilgi Kazancı (Information Gain)** girer.

**Odayı Temizlemek (Gini Mantığı):**
Bir odanın içinde 100 kişi var. Bunların 50'si bizi Terk Edecekler (Kırmızılar), 50'si de Sadıklar (Maviler). Oda şu an tamamen KARMAŞIK (Kirli) bir haldedir. Safsızlık (Gini Impurity) en üst seviyededir.
Sizin amacınız odayı bir soruyla ikiye bölmek ve oluşan iki odanın MÜMKÜN OLDUĞUNCA SAF (Sadece Kırmızılar veya Sadece Maviler) olmasını sağlamaktır.

- **Deneme 1 (Kötü Soru):** Ağaç "Cinsiyetiniz nedir?" diye bağırır. Kadınlar sağ odaya, erkekler sol odaya geçer. Sağ odaya bakarsınız; 25 Kırmızı, 25 Mavi vardır. Sol odada 25 Kırmızı, 25 Mavi vardır. Soru hiçbir işe yaramamıştır! Odalar hala kirli ve karışıktır. "Cinsiyet" sorusunun Bilgi Kazancı SIFIRDIR.
- **Deneme 2 (Mükemmel Soru):** Ağaç bu kez "Aylık sözleşmeniz mi var?" diye bağırır. "Evet" diyenler sağa, "Hayır" diyenler sola geçer. Sağ odaya (Aylıkçılar) bir bakarsınız: 45 Kırmızı, sadece 5 Mavi vardır! Sol odada ise 45 Mavi, sadece 5 Kırmızı vardır. Muazzam! Odalar neredeyse tertemiz, saf renklerine ayrılmıştır. Safsızlık (Gini) sıfıra yaklaşmıştır. 

İşte Karar Ağaçları arka planda her özellik için bu saflık temizliğini matematiksel olarak hesaplar. Odayı en temiz hale getiren, kirliliği en aza indiren o sihirli soruyu bulur ve EN TEPEYE onu çiviler. Ağaç böyle büyür.



## BÖLÜM 6: Rastgele Orman (Random Forest) - 1000 Doktorluk Heyet

Karar Ağaçları çok açıklanabilirdir ancak çok tehlikeli bir huyları vardır: **Overfitting (Ezberleme)**. Ağaç çok uzarsa, sadece 1 müşteriye ait olan çok saçma bir özelliği genel bir kural zannedip dallandırıp budaklandırabilir.

**Ağaçtan Ormana Geçiş:**
Bu sorunu çözmek için makine öğrenmesi mühendisleri muazzam bir felsefe geliştirmiştir: "Neden tek bir ağacın (doktorun) lafıyla hareket ediyoruz? Neden bir hastane dolusu doktor kurup oylama yaptırmıyoruz?" (Buna literatürde Ensemble Learning / Topluluk Öğrenmesi denir).

**Sistem Nasıl Çalışır?**
Veri setinizde 10.000 müşteri ve 50 farklı özellik var. Random Forest, tek bir devasa karar ağacı kurmak yerine, bilgisayarın hafızasında **1.000 farklı küçük Karar Ağacı** yaratır. 
Ancak her bir ağaca verinin tamamını göstermez! (Buna Bagging denir). 
Örneğin; 1. Ağaca rastgele 500 müşteri seçip verir, sadece "Fatura ve Yaş" özelliklerini gösterir. 2. Ağaca başka rastgele 500 müşteri verir, onlara da sadece "Sözleşme Tipi ve Cinsiyet" özelliklerini gösterir.
Böylece 1.000 tane, olayların sadece bir kısmını bilen, uzmanlık alanları farklı "yarı cahil" doktorlar ordusu oluşur.

**Oylama Günü (Demokrasi):**
Şirkete yepyeni bir müşteri geldi. Acaba churn olacak mı? 
Müşteri kapıdan içeri girer ve 1.000 ağaç aynı anda bu müşteriyi inceler. Sonra gizli oylama başlar.
- 870 Ağaç: "Bu adam BİZİ TERK EDECEK!" diye oy atar.
- 130 Ağaç: "Hayır, bu adam BİZDE KALACAK!" diye oy atar.

Sistem oyları sayar ve çoğunluk (Demokrasi) galip gelir. 130 tane ağaç tamamen yanlış özelliklere bakıp hata yapmış olsa bile, sistemin genel bilgeliği o hataları yutar ve ezer. Bu yüzden Random Forest, tek bir ağacın yapabileceği o ezberleme (overfitting) hatasını asla yapmaz ve makalelerde genellikle en stabil, en güvenilir model olarak zirveye oturur.



## BÖLÜM 7: Destek Vektör Makineleri (SVM) ve "Uzay Bükücü" Çekirdekler

Makalelerde (özellikle Vafeiadis vd. 2015) doğruluk oranını %96'lara taşıyan o ağır topa, SVM'e (Support Vector Machines) geldik. 
SVM, ağaçlar gibi soru sormaz. Komşulara bakmaz. SVM, veriyi tam ortadan "kılıçla kesen" bir algoritmadır.

**Mantığı (Misketlerin Arasına Çelik Duvar Örmek):**
Devasa bir masanın üzerinde olduğunuzu hayal edin. Masanın bir tarafında Mavi Misketler (Sadık Müşteriler), diğer tarafında Kırmızı Misketler (Terk Edenler) var. Sizin göreviniz, elinizdeki uzun çelik bir cetveli (Buna Hyperplane - Karar Sınırı denir) masanın üzerine öyle bir yerleştirmek ki, bütün kırmızılar cetvelin bir tarafında, bütün maviler diğer tarafında kalsın.
Ancak SVM'in takıntısı şudur: Bu cetveli sadece araya koyup bırakmaz. Cetveli, kırmızıların en ucundaki sınır misketine ve mavilerin en ucundaki sınır misketine **EŞİT UZAKLIKTA** ve **MÜMKÜN OLAN EN GENİŞ KORİDORU (Margin)** yaratacak şekilde konumlandırır. (O uçlardaki misketlere "Destek Vektörü - Support Vector" denmesinin sebebi budur, koca duvarı o birkaç misket destekler).

### 7.1. Ya Misketler İç İçe Geçmişse? (Kernel Trick / Çekirdek Hilesi)
Peki ya gerçek hayatta olduğu gibi müşteriler öyle masada iki ayrı tarafta durmuyorsa? Kırmızılar ve Maviler birbirinin içine, bir yumak gibi geçmişse? Siz masaya ne kadar düz cetvel koymaya çalışırsanız çalışın, hep birilerini yanlış tarafta bırakırsınız (Lineer olarak ayrılamayan veri).

İşte makalede harikalar yaratan **"SVM-POLY (Polinom)"** ve **"SVM-RBF"** mucizesi tam da burada başlar!
Matematikçiler der ki: "Eğer veriyi 2 boyutlu (masa düzlemi) ortamda dümdüz ayıramıyorsak, masaya alttan çok güçlü bir yumruk atarız!"
SVM'in Çekirdek Hilesi (Kernel Trick) tam olarak budur. Veriyi alır ve cebirsel bir formülle bir anda 3. boyuta, havaya fırlatır! 
O iç içe geçmiş misketler havada dağılır. Kırmızılar biraz daha yükseğe sıçrar, Maviler biraz daha aşağıda kalır. Misketler tam havadayken, SVM aralarından uçsuz bucaksız, dümdüz bir tepsiyi jilet gibi geçirir ve kırmızılarla mavileri HAVA BOŞLUĞUNDA ikiye ayırır.
Sonra yerçekimiyle misketler masaya (2 boyuta) geri düştüğünde, havada dümdüz olan o ayrım, masada sanki yuvarlak, inanılmaz kıvrımlı, mükemmel bir "S" veya "Daire" sınır çizgisiymiş gibi görünür. SVM'in bu uzay bükme yeteneği, onu dünyanın en sofistike, en keskin ayırıcı algoritmalarından biri yapar.



## BÖLÜM 8: Yapay Sinir Ağları (ANN) - Beyni Taklit Eden Kara Kutu

Makalelerde, insan zekasını en çok taklit ettiği için saygıyla anılan Yapay Sinir Ağları (Artificial Neural Networks - ANN).

**Nasıl Çalışır? (Beyin Hücreleri):**
Beynimizde nöronlar vardır. Gözümüzden gelen ışık sinyali ilk nörona çarpar, o nöron komşusuna bir elektrik gönderir, o komşusuna derken beynin arka tarafında "Bu bir elma" kararı oluşur.
ANN de tamamen böyledir.
- **Girdi Katmanı (Input Layer):** Müşterinin faturası, yaşı, şikayet sayısı buradaki nöronlara elektrik sinyali olarak girer.
- **Gizli Katmanlar (Hidden Layers):** Ortada yüzlerce dijital nöron vardır. "Fatura yüksekse ve yaş gençse A nöronunu %80 şiddetinde ateşle!" gibi kurallar vardır. Her nöron diğerine ağırlıklarla (weights) bağlıdır. Sinyaller bu karanlık ormanın içinde dolaşır, katlanır, küçülür, çarpılır...
- **Çıktı Katmanı (Output Layer):** En son bir ışık yanar ve makine "Bu müşteri %91 ihtimalle bizi Terk Edecek!" diye bağırır.

**En Büyük Sorun: "Kara Kutu" (Black Box) Olması:**
ANN, tahminleri %96 doğrulukla, mükemmele yakın yapar. Ancak büyük şirketlerin yönetim kurullarında sunum yaparken veri bilimcilerin kabusudur.
Müdür sorar: *"Ahmet Bey neden bizi terk edecekmiş? Sorun ne?"*
Karar Ağacı olsa "Çünkü DSL kullanıyor" derdiniz. Ancak ANN'de cevap veremezsiniz! Çünkü ANN size bir sebep sunmaz. Sadece içerideki o binlerce elektrik sinyalinin çarpım sonucunu sunar. Eğer *"Çünkü içerideki 45. gizli katmanın 12. nöronundaki aktivasyon fonksiyonu ateşlendiği için"* derseniz müdür sizi işten kovar. Sebebi açıklanamadığı için (Açıklanabilirlik eksikliği), aksiyon alınması gereken pazarlama kararlarında ANN'den genelde kaçılır, Ağaçlara yönelinir.



## BÖLÜM 9: AdaBoost ve XGBoost (Hatalardan Ders Alan Aptallar Ordusu)

Vafeiadis vd. (2015) makalesinin asıl yıldızı burasıdır. Yazarlar, zaten güçlü olan SVM'i alıp, **AdaBoost (Adaptive Boosting)** tekniğiyle birleştirmiş ve başarıyı %96.85'e, F-Ölçütünü %84.57'ye fırlatmıştır. Peki nedir bu Boosting (Güçlendirme)?

**Mantığı (Sırayla Çalışan Ordular):**
Random Forest'i hatırlayın. Orada 1.000 tane doktor vardı ve hepsi "Aynı Anda" oy kullanıyordu. Birbirlerinden haberleri yoktu.
Boosting sistemlerinde ise doktorlar "AYNI ANDA" değil, "SIRA SIRA" çalışırlar ve her gelen doktor, bir önceki doktorun **BATIRDIĞI** hastalara (hatalara) odaklanır. Bu muazzam bir "Hatalardan ders alma" felsefesidir.

**Adım Adım Nasıl Çalışır?**
1. Sistem, bilerek çok aptal, çok zayıf bir Karar Ağacı yaratır (Öyle ki, sadece tek bir soru sorabiliyordur).
2. Bu aptal ağaç, 100 müşterilik bir deneme yapar. Tabii ki aptal olduğu için 70'ini doğru bilir, 30'unu bilemez.
3. **İşte Sihir Zamanı:** AdaBoost, o bilemediği 30 "zor" müşteriyi alır ve onların sistemdeki ağırlığını (katsayısını) devasa şekilde artırır. Adeta bu zor müşterilerin isimlerinin altını Kırmızı Kalemle çizer.
4. Sistem ikinci bir aptal ağaç daha yaratır. İkinci ağaca der ki: *"Önceki ağacın doğru bildiklerini boşver, onlarla ilgilenme. Senin hayattaki tek amacın, şu altı kırmızıyla çizilmiş olan 30 zor müşteriyi doğru bilmektir!"*
5. İkinci ağaç o 30 kişiye odaklanır. 20'sini doğru bilir, 10'unda o da hata yapar.
6. AdaBoost hemen o 10 kişinin altını iki kez çizer, ağırlıklarını daha da artırır ve üçüncü ağacı çağırır...

Bu işlem yüzlerce kez tekrarlanır. Her yeni model, sadece ve sadece bir öncekilerin hata yaptığı o karmaşık, o "zor" müşterilerin zayıflıklarını çözmek üzerine uzmanlaşır. 
Günün sonunda yüzlerce aptal ağaçtan oluşan bu "Hatalardan ders alma zinciri" birbirine bağlandığında, dünyadaki hiçbir zor veriyi kaçırmayan, turnuvaları domine eden devasa bir makineye (AdaBoost, Gradient Boosting, XGBoost) dönüşür. Araştırmacılar bu yöntemi SVM ile desteklediklerinde sistem adeta müşteri kaybının DNA'sını çözmüş hale gelmiştir.



## BÖLÜM 10: Makineyi Sınava Sokmak (Overfitting ve Çapraz Doğrulama)

Bütün modelleri kurduk. Makinenin ekranda "Başarı oranım %99" yazdığını gördünüz. Sevinmeli miyiz? Hayır, dehşete düşmeliyiz. Çünkü makine büyük ihtimalle "Overfitting" (Aşırı Öğrenme/Ezberleme) tuzağına düşmüştür.

### 10.1. Overfitting (Ezberlemek) ve Underfitting (Aptallık)
- **Underfitting (Eksik Öğrenme):** Makine o kadar aptaldır ki, verinin içindeki kuralları çıkaramamıştır. Müşteri zengin mi, fakir mi umursamaz, herkese "Bu adam churn olacak" der geçer.
- **Overfitting (Aşırı Öğrenme / Papağanlık):** Makine veriyi ve müşterileri öyle bir inceler ki, genel kuralları bulmak yerine istisnaları ezberler. Öğrenci mantığıyla düşünün: Öğrenci evde deneme sınavını çözerken matematiğin mantığını anlamak yerine, "Cevapların sırası A-B-C-A-D'dir" diye ezberlemiştir. Evdeki sınavından %100 alır. Ama gerçek sınava, yani daha önce **Hiç Görmediği** yeni soruların olduğu sınava girince sıfır çeker.
Makine öğrenmesinde de model size geçmiş müşterilerde %100 başarı gösterir ama yarın kapıdan yeni bir müşteri girdiğinde çuvallar.

### 10.2. Çözüm: K-Fold Cross Validation (10 Katlı Çapraz Doğrulama)
Peki makinenin konuyu gerçekten anladığını (Genelleştirme - Generalization yapabildiğini) nasıl test edeceğiz? Onu ardı ardına 10 farklı deneme sınavına sokarak! Buna K-Fold Çapraz Doğrulama denir.

Elinizde 10.000 müşteri var. Bunu 10 eşit klasöre bölersiniz (Her birinde 1.000 müşteri).
- **1. Sınav:** Makine ilk 9 klasördeki 9.000 kişiyle ders çalışır (Eğitim - Train). Sonra hayatında ilk defa göreceği o 10. klasördeki 1.000 müşteriyle sınava girer (Test). Notunu alır (Örn: %92).
- **2. Sınav:** Sonra hafızasını siler. Bu kez klasörlerin yerini değiştiririz. Makine farklı 9 klasörle ders çalışır, farklı bir klasörle teste girer. Notunu alır (Örn: %89).
Bu işlem 10 kez, 10 farklı kombinasyonla tekrarlanır.
En sonunda bu 10 sınavın ortalaması alınır. Eğer makine gerçekten "zeki" ise ve ezber yapmıyorsa, her sınavdan birbirine yakın ve yüksek notlar alır. İşte akademik makalelerde size "Bu model %96 başarılı" deniyorsa, bilin ki bu tek bir sınavın değil, bu zorlu Çapraz Doğrulama cehenneminden çıkmış 10 sınavın ortalamasıdır. O başarı gerçektir.



## BÖLÜM 11: Başarı Yanılsaması (Neden %99 Doğruluk Şirketi Batırır?)

İşte makalelerde (Lalwani vd.) en çok üstünde durulan, bir şirketin hayatını kurtaracak o kritik kavramlar: **Confusion Matrix (Karmaşıklık Matrisi), Recall, Precision, F1-Score ve ROC/AUC.**

**Dengesiz Verinin Dehşeti:**
Sizin Telekom şirketinizde 10.000 müşteri var. Bunların 9.500'ü mutlu (Sadık), sadece 500'ü kızgın ve gidici (Churn). Buna **Dengesiz Veri (Imbalanced Data)** denir.
Bir makine öğrenmesi modeli kurdunuz. Makine çok tembel çıktı ve dedi ki: *"Aman ne uğraşacağım! Ben ekrana BÜTÜN MÜŞTERİLER KALACAK diye sonuç yazayım, bitsin gitsin."*
Makine bu tahmini yaptı. Sonuçları kontrol ettiniz:
- O mutlu olan 9.500 kişiyi "Kalacak" diyerek DOĞRU BİLDİ.
- Gidecek olan 500 kişiye de "Kalacak" dediği için YANLIŞ BİLDİ.
Toplamda 10.000 kişinin 9.500'ünü doğru bilmiş oldu. 
Hesap makinesini açtınız, Doğruluk (Accuracy) Oranı = **%95!**
"Muazzam! Dünyanın en iyi yapay zekasını kurduk!" deyip şampanyaları patlattınız.

**Peki Gerçekte Ne Oldu? Şirketiniz Battı!**
Çünkü sizin asıl bulmanız gereken, acil müdahale etmeniz gereken o 500 kaçak müşterinin HİÇBİRİNİ (Sıfırını) bulamadınız. Accuracy oranının nasıl devasa bir YALAN olduğunu gördünüz mü? İşte bu yalanı ortaya çıkarmak için Karmaşıklık Matrisi ve yeni metrikler devreye girer.

### 11.1. Karmaşıklık Matrisi (4 Kutu)
Tahminleri 4 kutuya ayırır:
1. **True Positive (TP):** Gerçekten gideni "Gidiyor" diye yakaladıklarımız (Harika!).
2. **True Negative (TN):** Gerçekten kalanı "Kalıyor" dediklerimiz (Zaten mutlular).
3. **False Positive (FP - Yalancı Çoban):** Aslında kalacak olan ama makinenin "Bu adam gidiyor!" diye yalan alarm verdikleri. (Bu adamlara boş yere hediye çeki verip şirketi zarara sokarsınız).
4. **False Negative (FN - Faciâ):** Aslında GİDEN ama makinenin "Yok ya bu adam güvenli, kalıyor" deyip gözden kaçırdıkları. (Şirketi asıl batıran delik burasıdır).

### 11.2. Recall (Duyarlılık - Tehlikeyi Kaçırmamak)
Formülü: `TP / (TP + FN)`. Meali: "Gerçekten kapıya doğru yürüyüp giden insanların YÜZDE KAÇINI yakalayabildik?"
Telekom ve Tıp dünyası Recall'a tapar. Neden mi? Çünkü kanser taraması yapan bir makine, hastalıklı birini "Sen sağlıklısın" (False Negative) diye eve gönderirse o hasta ölür. Telekom'da da değerli bir müşteriyi gözden kaçırmak affedilemez. Eğer %95 Accuracy olan o tembel modelin Recall'unu hesaplarsak sonuç SIFIR çıkar. Anında çöpe atarsınız.

### 11.3. Precision (Kesinlik - Attığını Vurmak)
Formülü: `TP / (TP + FP)`. Meali: "Makine kırmızı alarm verip 'Şu 100 kişi gidiyor' dedi. İyi de makinenin alarm verdiği bu 100 kişinin kaçı GERÇEKTEN gidiyor?"
Eğer makine çok korkaksa, herkese "Bu adam gidiyor!" diye alarm öttürür (Sürekli False Positive üretir). Eğer Precision düşükse, sisteminiz yalancı çobana dönmüştür. Herkese bedava internet teklif edip şirketi milyarlarca lira zarara sokarsınız.

### 11.4. F1-Score ve ROC/AUC (Büyük Denge)
- **F1-Score:** Pazarlama yöneticisi veri bilimciye der ki: *"Bana öyle bir model kur ki, hem gidenleri gözden kaçırmasın (Yüksek Recall), hem de yalancı çobanlık yapıp beni zarara sokmasın (Yüksek Precision)."* İşte bu ikisinin tam ortasını bulan, modelin gerçek kalitesini gösteren muazzam puana F1-Score denir.
- **ROC/AUC Eğrisi:** Radyo frekans ayarı gibidir. Düğmeyi sağa çevirirsiniz (Sistemi hassaslaştırırsınız), kimseyi kaçırmazsınız ama çok yalan alarm verirsiniz. Sola çevirirsiniz, yalan alarm biter ama gidenleri kaçırırsınız. ROC Eğrisi, bir modelin bu düğmeyle oynandığında yeteneğini nasıl koruduğunu gösteren bir savaş haritasıdır. Çizginin altındaki alan (AUC) ne kadar %100'e yakınsa, o makine o kadar kusursuz bir radardır.



## BÖLÜM 12: 6 Aşamalı Churn Tahmin Fabrikası ve SMOTE Klonları

Praveen Lalwani ve arkadaşlarının (2021) IBM Watson verisi üzerinde kurduğu sistem, makine öğrenmesinin akademik havadan çıkıp "Fabrika" mantığına oturduğu yerdir. Veri havadan alınıp hemen SVM'e verilmez. 6 aşamadan geçerek rafine edilir:

1. **Veri Seçimi:** 7043 müşterinin 21 özelliği ham bir şekilde alınır.
2. **Veri Ön İşleme (Preprocessing):** Müşteri formda yaşını boş bırakmıştır (Kayıp Veri). Makine boşluk görünce çöker. Veri bilimci o boşluğu, diğer tüm müşterilerin yaş ortalamasını alarak (Örn: 35) doldurur. Sonra cinsiyet sütunundaki "Kadın/Erkek" kelimelerini makinenin okuyabileceği "1 ve 0"lara dönüştürür (Encoding).
3. **Özellik Seçimi (Feature Selection):** Müşterinin Posta Kodu churn'ü etkiler mi? Etkilemez. Bu gereksiz bilgileri (gürültüyü) veriden kesip atarak makinenin kafasının karışmasını önlerler.
4. **Sentetik Veri Üretimi (SMOTE):** BÖLÜM 11'de bahsettiğimiz o 9.500 Sadık, 500 Terk Eden dengesizliğini çözmek için en muazzam adımdır. Model tembellik etmesin diye, SMOTE algoritması devreye girer. O giden 500 müşterinin özelliklerine bakar ve tamamen bilgisayar ortamında, hayali (Sentetik) 9.000 tane daha kötü müşteri KLONLAR. Terazinin iki kefesi (9.500 İyi, 9.500 Kötü) eşitlenir. Makine artık paşa paşa "Kötü" müşterilerin DNA'sını öğrenmek zorundadır.
5. **Modelin Eğitilmesi:** Temizlenen ve dengelenen bu muazzam veri, Karar Ağaçları veya AdaBoost gibi algoritmalara yedirilir.
6. **Değerlendirme:** Recall ve F1-Score metrikleriyle model teste tabi tutulur.



## BÖLÜM 13: ASOS.com ve Müşterinin Ruhunu "Embedding" İle Çözmek

Gelelim son makaleye. Klasik Telekom dünyasını, kontratları ve faturaları unutup e-ticaretin en tepe noktasına, İngiliz giyim devi ASOS.com'a gidiyoruz. 
Klasik modeller sadece "Müşteri ne kadar harcadı? Ne kadar sıklıkla geldi?" (RFM mantığı) diye bakar. ASOS'un veri bilimcileri 2017'de şu inanılmaz soruyu sorar: **"Müşterinin NE TARZ şeyler aldığı, onun bize gelecekte ne kazandıracağını (CLV) belirlemez mi?"**

**Word2Vec'ten Ürün Uzayına (Kelime Matematiği):**
Google, "Word2Vec" adında bir algoritma bulmuştu. Kelimelerin cümle içindeki yakınlığına bakarak onları 3 Boyutlu devasa bir uzaya atıyordu. Örneğin "Kral" ve "Erkek" uzayda yan yana duruyordu. 
ASOS bunu aldı ve kıyafetlere uyarladı!
Müşterilerin alışveriş sepetlerini bir "Cümle", içindeki kıyafetleri "Kelime" olarak gördüler.
Bir müşteri her seferinde Siyah Dar Kot'un yanına Deri Ceket ekliyorsa, makine "Siyah Kot" ile "Deri Ceket"i uzayda (Embedding Space) birbirine kenetledi. "Pembe Çiçekli Elbise"yi ise uzayın bambaşka, çok uzak bir ucuna fırlattı.

**Müşteriyi Uzaya Fırlatmak:**
Kıyafetler uzaya yerleştikten sonra, ASOS "Müşteri Ahmet'i" alıp bu uzayın içine fırlatır! Ahmet'in geçmişte aldığı şeylere bakarak, Ahmet uzayda deri ceketlerin, asi ve koyu renkli kıyafetlerin olduğu mahalleye düşer.
Artık ASOS, Ahmet'i "Toplam 500 TL harcayan bir müşteri" olarak değil, "Deri ceket bölgesinde yaşayan, rock tarzı bir müşteri" olarak (vektörel sayılarla) kaydeder.

**Bu Neden Mükemmeldir?**
Çünkü kıyafet e-ticaretinde şirketi batıran şey müşterinin aldığı ürünleri **İADE** etmesidir (Ücretsiz iade kargosu şirkete zarar yazar). Ve ASOS şunu çok iyi bilir: Düğünlük Abiye alan bir kadının o kıyafeti düğünden sonra iade etme ihtimali çok yüksektir. Ancak günlük deri ceket alan bir gencin iade ihtimali düşüktür.
ASOS'un Random Forest modeli, müşterinin uzaydaki o tarzına, koordinatına (Embedding vektörlerine) bakarak CLV (Yaşam Boyu Değer) tahminini muazzam bir isabetle yapar. Sadece rakamlara değil, "Müşterinin Ruhuna ve Tarzına" göre tahmin yapmanın dünyadaki en ileri seviyesidir.



## BÖLÜM 14: Sonuç, Büyük Çıkarımlar ve Yöneticiler İçin Dersler

Bu koca klasörün içindeki onca algoritmadan, SVM'lerden, uzay bükülmelerinden ve AdaBoost ordularından yöneticilerin ve veri bilimcilerin cebine koyup götürmesi gereken son hayat dersleri şunlardır:

1. **Hiçbir Algoritma Sihirli Değildir (Garbage in, Garbage Out):** Eğer veriniz çöp gibi düzensizse, müşterilerin yaşları eksikse, SMOTE ile o dengesizlik çözülmemişse isterseniz NASA'nın Yapay Sinir Ağlarını getirin, model çöker. Temizlik (Preprocessing) her şeydir.
2. **Kara Kutu (ANN) vs. Açıklanabilirlik (Karar Ağaçları) Savaşı:** Bir banka müdürüne "Müşteri gidecek çünkü içerideki nöron ateşlendi" derseniz sizi dinlemez. Aksiyon almak, o müşteriyi arayıp özür dilemek istiyorsanız size "Sebebi" lazımdır. Bu yüzden en yüksek başarıyı SVM veya ANN verse bile, şirketler %3-%5 daha az başarılı ama derdini anlatabilen Karar Ağaçlarına (Decision Trees) ve Random Forest'a mecburen dönerler.
3. **Doğruluk (Accuracy) Yalanına Kanmayın:** Bir veri bilimci size sırıtarak "Sistemimiz %99 doğru çalışıyor" dediğinde, hemen masaya vurun ve sorun: **"Benim için Doğruluğu geç, senin modelin Recall (Gidenleri kaçırmama) ve F1-Skoru kaç?"** Eğer bunları söyleyemiyorsa, o model muhtemelen hiçbir kaçağı bulamayan tembel bir sistemdir.
4. **Gelecek Körlüğü:** Malthouse'un makalesinde uyardığı gibi, makine öğrenmesi sadece BUGÜNÜN fotoğrafını çeker. Bugün uzay vektörlerinde mükemmel bir noktada olan müşteri yarın iflas edebilir. Modeller yüzde yüz bilecek sihirli küreler değildir, onlar sadece kaotik insan doğasında riskimizi düşüren ve bize fener tutan harika matematiksel olasılık makineleridir.


