import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\emink\Downloads\BankChurners\BankChurners.csv")
print(df.shape)
print(df.columns.tolist())


print("\n--- KOLON SİLME ---")
print("Silmeden önce:", df.shape)

# 1) Naive Bayes kolonlarını bul (isimleri çok uzun, startswith ile yakalıyoruz)
nb_cols = [col for col in df.columns if col.startswith("Naive_Bayes")]
print("Naive Bayes kolonları:", nb_cols)

# 2) Silinecek kolonları bir listeye topla
drop_list = ["Avg_Open_To_Buy"] + nb_cols

# 3) Drop et
df = df.drop(columns=drop_list)

print("Sildikten sonra:", df.shape)
print("Kalan kolonlar:", df.columns.tolist())
# Zayif kolonlari sil (ama Card_Category ve Education_Level KALACAK)
weak_cols = ["Customer_Age", "Months_on_book", "Dependent_count",
             "Gender", "Marital_Status", "Income_Category"]

df = df.drop(columns=weak_cols)
print("Sildikten sonra:", df.shape)
print("Kalan kolonlar:", df.columns.tolist())

print("\n--- FEATURE ENGINEERING ---")

# 1) Ortalama islem buyuklugu: Musteri baska baska kucuk mu harcıyor yoksa tek seferde buyuk mu?
df["Avg_Trans_Value"] = df["Total_Trans_Amt"] / df["Total_Trans_Ct"]

# 2) Aktiflik orani: 12 aydan kac ay aktifti?
df["Activity_Rate"] = (12 - df["Months_Inactive_12_mon"]) / 12

# 3) Kullanim yogunlugu: Limiti ne kadar dolduruyor (revolving / limit)
df["Revolving_to_Limit"] = df["Total_Revolving_Bal"] / df["Credit_Limit"]

# 4) Islem basina limit: Musterinin limiti islem sayisina gore ne kadar buyuk?
df["Limit_per_Trans"] = df["Credit_Limit"] / df["Total_Trans_Ct"]

# 5) Degisim skoru: Hem tutar hem adet degisimini birlestir
df["Change_Score"] = df["Total_Amt_Chng_Q4_Q1"] * df["Total_Ct_Chng_Q4_Q1"]

print("Yeni kolonlar eklendi!")
print("Guncel shape:", df.shape)
print("Tum kolonlar:", df.columns.tolist())

print("\n--- ENCODING ---")

# 1) Target: Attrition_Flag -> 0/1
df["Attrition_Flag"] = df["Attrition_Flag"].map({
    "Existing Customer": 0,
    "Attrited Customer": 1
})
print("Target encoded:", df["Attrition_Flag"].value_counts().to_dict())

# 2) Education_Level -> Ordinal (sirali encoding)
edu_order = {"Uneducated": 0, "High School": 1, "College": 2,
             "Graduate": 3, "Post-Graduate": 4, "Doctorate": 5, "Unknown": 3}
df["Education_Level"] = df["Education_Level"].map(edu_order)

# 3) Card_Category -> Ordinal (prestij sirasi)
card_order = {"Blue": 0, "Silver": 1, "Gold": 2, "Platinum": 3}
df["Card_Category"] = df["Card_Category"].map(card_order)

print("Encoding tamamlandi!")
print("Dtypes:\n", df.dtypes)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

print("\n--- SCALING & SPLIT ---")

# Target ve feature'lari ayir (CLIENTNUM modele girmez)
X = df.drop(columns=["Attrition_Flag", "CLIENTNUM"])
y = df["Attrition_Flag"]

print("X shape:", X.shape)
print("y dagilimi:\n", y.value_counts())

# Train/Test split (%80/%20, stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTrain:", X_train.shape, "Test:", X_test.shape)

# Scaling (sadece train'den ogren, test'e uygula -> leakage onleme)
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

print("Scaling tamamlandi!")
print("\nTrain ortalamalar (0'a yakin olmali):")
print(X_train_scaled.mean().round(2).to_string())

print("\n--- KAYDETME ---")

# CSV olarak kaydet
X_train_scaled.to_csv(r"C:\Users\emink\Desktop\zorunlu staj\preprocessing\X_train.csv", index=False)
X_test_scaled.to_csv(r"C:\Users\emink\Desktop\zorunlu staj\preprocessing\X_test.csv", index=False)
y_train.to_csv(r"C:\Users\emink\Desktop\zorunlu staj\preprocessing\y_train.csv", index=False)
y_test.to_csv(r"C:\Users\emink\Desktop\zorunlu staj\preprocessing\y_test.csv", index=False)

print("X_train:", X_train_scaled.shape, "-> X_train.csv")
print("X_test:", X_test_scaled.shape, "-> X_test.csv")
print("y_train:", y_train.shape, "-> y_train.csv")
print("y_test:", y_test.shape, "-> y_test.csv")
print("\nTum dosyalar preprocessing klasorune kaydedildi!")