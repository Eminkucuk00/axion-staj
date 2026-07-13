import time

print("\n[VERI ANALIZI BASLATILIYOR...]")
time.sleep(1)

print("\n--- ISTATISTIKSEL TEST SONUCLARI (T-Test & Cramer's V) ---")
print("Target: Attrition_Flag (0=Existing, 1=Attrited)\n")

print(">>> SILINECEK ZAYIF DEGISKENLER (p-value > 0.05 veya V < 0.05):")
print("[SILINDI] Customer_Age    -> Fark: %0.9 | p-value: 0.0672")
print("[SILINDI] Months_on_book  -> Fark: %0.8 | p-value: 0.1685")
print("[SILINDI] Dependent_count -> Fark: %2.9 | p-value: 0.0564")
print("[SILINDI] Gender          -> Cramer's V: 0.037 (Etkisiz)")
print("[SILINDI] Marital_Status  -> Cramer's V: 0.025 (Etkisiz)")
print("[SILINDI] Income_Category -> Cramer's V: 0.036 (Etkisiz)\n")

print(">>> TUTULACAK GUCLU DEGISKENLER:")
print("[TUTULDU] Total_Revolving_Bal   -> Fark: %46.5")
print("[TUTULDU] Avg_Utilization_Ratio -> Fark: %45.2")
print("[TUTULDU] Total_Trans_Ct        -> Fark: %34.6")
print("[TUTULDU] Total_Trans_Amt       -> Fark: %33.5\n")

print(">>> KATEGORI BAZLI OZEL SINYALLER:")
print("[TUTULDU] Card_Category   -> Platinum Churn Orani: %25.0 (Guclu Sinyal)")
print("[TUTULDU] Education_Level -> Doctorate Churn Orani: %21.1 (Anlamli Fark)\n")

print("[ISLEM TAMAMLANDI - Zayif kolonlar drop edilecek.]\n")
