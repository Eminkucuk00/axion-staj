import pandas as pd
import streamlit as st

@st.cache_data
def veri_yukle():
    """
    Instacart veri setlerini okur, temizler ve birleştirir.
    Performans için @st.cache_data ile önbelleğe alınır.
    """
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        siparisler = pd.read_csv(os.path.join(base_dir, "data", "orders.zip"))
        sepet_icerigi = pd.read_csv(os.path.join(base_dir, "data", "order_products__train.zip"))
        urunler = pd.read_csv(os.path.join(base_dir, "data", "products.zip"))
    except FileNotFoundError:
        st.error("Veri dosyaları bulunamadı. Lütfen 'data/' klasörünün içinde doğru CSV dosyalarının olduğundan emin olun.")
        st.stop()

    temiz_sepet_datasi = pd.merge(sepet_icerigi, urunler[['product_id', 'product_name']], on='product_id', how='left')
    
    ana_veri = pd.merge(
        temiz_sepet_datasi, 
        siparisler[['order_id', 'order_dow', 'order_hour_of_day', 'days_since_prior_order']], 
        on='order_id', 
        how='left'
    )
    
    return ana_veri, siparisler

def veriyi_filtrele(df, secilen_gun, secilen_saat):
    """
    Kullanıcının Sidebar'da seçtiği filtreleri uygular.
    """
    filtrelenmis = df.copy()
    
    # Gün Filtresi
    if secilen_gun == "Hafta İçi":
        filtrelenmis = filtrelenmis[filtrelenmis['order_dow'].isin([2, 3, 4, 5, 6])]
    elif secilen_gun == "Hafta Sonu":
        filtrelenmis = filtrelenmis[filtrelenmis['order_dow'].isin([0, 1])]
        
    # Saat Filtresi
    if secilen_saat == "Sabah (06-12)":
        filtrelenmis = filtrelenmis[(filtrelenmis['order_hour_of_day'] >= 6) & (filtrelenmis['order_hour_of_day'] < 12)]
    elif secilen_saat == "Öğle (12-18)":
        filtrelenmis = filtrelenmis[(filtrelenmis['order_hour_of_day'] >= 12) & (filtrelenmis['order_hour_of_day'] < 18)]
    elif secilen_saat == "Akşam (18-24)":
        filtrelenmis = filtrelenmis[(filtrelenmis['order_hour_of_day'] >= 18) | (filtrelenmis['order_hour_of_day'] < 6)]
        
    return filtrelenmis

@st.cache_data
def association_rules_hesapla(df):
    """
    Filtrelenmiş veriye göre sepet analizi kurallarını hesaplar.
    """
    from mlxtend.frequent_patterns import fpgrowth
    from mlxtend.frequent_patterns import association_rules
    import pandas as pd

    # Kural 3: Orijinal notebook'taki gibi ilk 10.000 ürünü alıyoruz (Gereksiz sampling yapmıyoruz)
    populer_urunler = df['product_name'].value_counts().head(10000).index
    analiz_verisi = df[df['product_name'].isin(populer_urunler)]
    
    from mlxtend.preprocessing import TransactionEncoder
    
    # OOM (Out of Memory) çökmesini engellemek için unstack (yoğun matris) yerine
    # doğrudan seyrek (sparse) matris oluşturan TransactionEncoder kullanıyoruz.
    islemler = analiz_verisi.groupby('order_id')['product_name'].apply(list).values
    
    te = TransactionEncoder()
    te_ary = te.fit(islemler).transform(islemler, sparse=True)
    sepet_matrisi = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=te.columns_)
    
    frequent_itemsets = fpgrowth(sepet_matrisi, min_support=0.01, use_colnames=True)
    
    if len(frequent_itemsets) == 0:
        return pd.DataFrame()
        
    kurallar = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    
    kurallar['antecedents'] = kurallar['antecedents'].apply(lambda x: ', '.join(list(x)))
    kurallar['consequents'] = kurallar['consequents'].apply(lambda x: ', '.join(list(x)))
    
    return kurallar
