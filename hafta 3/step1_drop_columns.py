"""
=============================================================
SPRINT 5 - Feature Engineering & Preprocessing Pipeline
BankChurners Dataset — Kredi Kartı Müşteri Kaybı Analizi
=============================================================
Mehmet Emin Küçük | AXION Staj Projesi
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# ADIM 0: VERİYİ YÜKLE
# ============================================================
print("=" * 60)
print("ADIM 0: Veri Yükleniyor...")
print("=" * 60)

df = pd.read_csv(r"C:\Users\emink\Downloads\BankChurners\BankChurners.csv")
print(f"✅ Ham veri yüklendi: {df.shape[0]} satır × {df.shape[1]} kolon")
print(f"   Kolonlar: {df.columns.tolist()}")


# ============================================================
# ADIM 1 (TASK 2): GEREKSİZ / LEAKAGE KOLONLARINI SİL
# ============================================================
print("\n" + "=" * 60)
print("ADIM 1: Gereksiz / Leakage Kolonlarını Silme")
print("=" * 60)

# ╔══════════════════════════════════════════════════════════╗
# ║  EMİN — BU KISMI SEN DOLDUR!                            ║
# ║                                                          ║
# ║  Aşağıda 4 kolon var. Her birini neden sildiğini         ║
# ║  kendi cümlelerinle yaz.                                 ║
# ╚══════════════════════════════════════════════════════════╝

# Silinecek kolonlar ve gerekçeleri:
kolonlar_silinecek = {
    "CLIENTNUM": "BURAYA GEREKÇENİ YAZ — İpucu: Modele ne katkı sağlar mı?",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1": "BURAYA GEREKÇENİ YAZ — İpucu: Bu kolon nereden gelmiş?",
    "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2": "BURAYA GEREKÇENİ YAZ — İpucu: Aynı risk burada da var",
    "Avg_Open_To_Buy": "BURAYA GEREKÇENİ YAZ — İpucu: Credit_Limit ile arasında ne var?"
}

print("\n📋 Silinecek kolonlar ve gerekçeleri:")
print("-" * 50)
for kolon, gerekce in kolonlar_silinecek.items():
    kolon_kisa = kolon[:40] + "..." if len(kolon) > 40 else kolon
    print(f"  ❌ {kolon_kisa}")
    print(f"     Gerekçe: {gerekce}")
    print()

# Drop işlemi
df_clean = df.drop(columns=list(kolonlar_silinecek.keys()))
print(f"✅ Silme sonrası: {df_clean.shape[0]} satır × {df_clean.shape[1]} kolon")
print(f"   Silinen kolon sayısı: {len(kolonlar_silinecek)}")
print(f"   Kalan kolonlar: {df_clean.columns.tolist()}")


# ============================================================
# DOĞRULAMA: Korelasyon Kontrolü
# ============================================================
print("\n" + "=" * 60)
print("DOĞRULAMA: Multicollinearity Kontrolü")
print("=" * 60)

# Sadece sayısal kolonları al
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
corr_matrix = df_clean[numeric_cols].corr()

# Yüksek korelasyonlu çiftleri bul (|r| > 0.8)
print("\n⚠️  Yüksek korelasyonlu çiftler (|r| > 0.80):")
print("-" * 50)
high_corr_found = False
for i in range(len(numeric_cols)):
    for j in range(i+1, len(numeric_cols)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.80:
            high_corr_found = True
            print(f"  🔴 {numeric_cols[i]} ↔ {numeric_cols[j]}: r = {r:.4f}")

if not high_corr_found:
    print("  ✅ Kritik düzeyde multicollinearity tespit edilmedi!")

# Korelasyon heatmap kaydet
plt.figure(figsize=(14, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8})
plt.title('Korelasyon Matrisi (Leakage & Multicollinearity Temizliği Sonrası)', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(r"C:\Users\emink\Desktop\zorunlu staj\preprocessing\korelasyon_matrisi.png", 
            dpi=150, bbox_inches='tight')
plt.close()
print("\n📊 Korelasyon heatmap kaydedildi: preprocessing/korelasyon_matrisi.png")

print("\n" + "=" * 60)
print("ADIM 1 TAMAMLANDI ✅")
print("=" * 60)
print(f"\nSonraki adım: ADIM 2 — Eksik Değer Yaklaşımı")
print("Bu scripti çalıştır ve çıktıları kontrol et!")
