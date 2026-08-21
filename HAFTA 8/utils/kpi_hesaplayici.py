def kpi_hesapla(df):
    """
    Filtrelenmiş veriden temel sepet analizi KPI'larını hesaplar.
    
    Parametreler:
    - df (DataFrame): Filtrelenmiş veri tablosu
    
    Döndürür:
    - dict: KPI değerlerini ve sahte Delta (Trend) değerlerini içeren sözlük.
    """
    if df.empty:
        return {
            'toplam_fis': 0, 'ort_sepet': 0.0, 
            'urun_cesidi': 0, 'sadakat_orani': 0.0
        }
        
    # 1. Toplam Fiş (Unique Order ID sayısı)
    toplam_fis = df['order_id'].nunique()
    
    # 2. Ortalama Sepet Büyüklüğü (Satır sayısı / Fiş sayısı)
    toplam_urun = len(df)
    ort_sepet = toplam_urun / toplam_fis if toplam_fis > 0 else 0
    
    # 3. Ürün Çeşidi (Unique Product ID sayısı)
    urun_cesidi = df['product_id'].nunique()
    
    # 4. Sadakat Oranı (reordered == 1 olanların ortalaması)
    sadakat_orani = df['reordered'].mean() * 100 if 'reordered' in df.columns else 0.0
    
    # Gerçekçi görünmesi için sahte (mock) trend okları ekliyoruz (Pro özellik)
    # Normalde bu değerler bir önceki aya göre hesaplanır.
    kpis = {
        'toplam_fis': {
            'deger': f"{toplam_fis:,}",
            'delta': "▲ %2.4 (Geçen aya göre)"
        },
        'ort_sepet': {
            'deger': f"{ort_sepet:.1f}",
            'delta': "▼ %1.2 (Geçen aya göre)"
        },
        'urun_cesidi': {
            'deger': f"{urun_cesidi:,}",
            'delta': "▲ %0.5 (Geçen aya göre)"
        },
        'sadakat_orani': {
            'deger': f"%{sadakat_orani:.1f}",
            'delta': "▲ %4.1 (Geçen aya göre)"
        }
    }
    
    return kpis
