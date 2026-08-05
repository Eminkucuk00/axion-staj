import pandas as pd
import numpy as np
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore")


def preprocess_data(df_raw):
    print("1.Veri Ön İşleme (Preprocessing) Başlıyor...")
    df = df_raw.copy()

    # ADIM A: Özellik Mühendisliği 
    df["Avg_Trans_Value"] = df["Total_Trans_Amt"] / df["Total_Trans_Ct"]
    df["Activity_Rate"] = (12-df["Months_Inactive_12_mon"]) / 12
    df["Revolving_to_limit"] = df["Total_Revolving_Bal"] / df["Credit_Limit"]
    df["Limit_per_Trans"] = df["Credit_Limit"] / df["Total_Trans_Ct"]
    df["Change_Score"] = df["Total_Amt_Chng_Q4_Q1"] * df["Total_Ct_Chng_Q4_Q1"]

    # ADIM B: Gereksiz Kolonların Silinmesi
    silinecekler = [
        'Avg_Open_To_Buy', 'Customer_Age', 'Dependent_count', 'Gender', 'Marital_Status', 'Income_Category', 'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1', 'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2'
    ]
    df = df.drop(columns=[c for c in silinecekler if c in df.columns], errors='ignore')

     # ADIM C: Hedef Değişken ve Kurallar
    df['Gercek_Durum'] = df['Attrition_Flag'].map({'Existing Customer':0, 'Attrited Customer': 1})
    df = df.drop('Attrition_Flag', axis=1)

    df['Education_Level'] = df['Education_Level'].replace('Unknown', '-1')

    kategorik_kolonlar= df.select_dtypes(include=['object']).columns.tolist()
    df_encoded = pd.get_dummies(df, columns=kategorik_kolonlar, drop_first=False)

    return df_encoded

def main():
    # 1. VERİYİ YÜKLE VE HAZIRLA
    veri_yolu = "BankChurners.csv"
    df_orijinal = pd.read_csv(veri_yolu)
    df_hazir = preprocess_data(df_orijinal)
    print(f"   İşlenmiş Veri Boyutu: {df_hazir.shape}")

    # 2. VERİYİ BÖL (Eğitim ve Test)
    print("2. Veri Bölme ve Ölçeklendirme İşlemleri")
    X = df_hazir.drop(columns=['Gercek_Durum', 'CLIENTNUM'])
    y = df_hazir['Gercek_Durum']
    client_ids = df_hazir['CLIENTNUM']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 3. STANDARD SCALER (Ölçeklendirme)
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    # 4. SMOTE (Sadece Eğitim Seti)
    print("3. SMOTE Uygulanıyor ve Model Eğitiliyor...")
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

    # 5. XGBOOST MODEL EĞİTİMİ (0.40 Eşik değeri ve max_depth=6)

    final_model = XGBClassifier(
        random_state=42,
        learning_rate=0.1,
        max_depth=6,
        n_estimators=100,
        eval_metric='logloss'
    )
    final_model.fit(X_train_smote, y_train_smote)
    print("   Model Başarıyla Eğitildi!")

    
    # 6. TÜM 10.127 MÜŞTERİYİ SKORLAMA ve SHAP ANALİZİ
    print("4. Tum musteriler skorlaniyor ve SHAP Analizi yapiliyor...")
    X_all = df_hazir.drop(columns=['Gercek_Durum', 'CLIENTNUM'])
    X_all_scaled = pd.DataFrame(scaler.transform(X_all), columns=X_all.columns)
    y_probs = final_model.predict_proba(X_all_scaled)[:, 1]


    # SHAP - Her müşteri için Ana Risk Nedenini bulma
    explainer = shap.TreeExplainer(final_model)
    shap_values = explainer.shap_values(X_all_scaled)

    if isinstance(shap_values, list):
        churn_shap_values = shap_values[1]
    else:
        churn_shap_values = shap_values

    ana_risk_nedenleri = []
    for i in range(len(churn_shap_values)):
        en_etkili_index = np.argmax(churn_shap_values[i])
        ana_risk_nedenleri.append(X_all_scaled.columns[en_etkili_index])

    # 7. ÇIKTI TABLOSU ÜRETİMİ (10.127 MÜŞTERİ)
    print("5. Müşteri Risk Çıktı Tablosu Oluşturuluyor...")
    output_df = pd.DataFrame()
    output_df["Musteri_ID"] = client_ids.values
    output_df["Churn_Probability"] = np.round(y_probs, 3)
    output_df["Gercek Durum"] = y.values   

    # Segmentasyon (Eşik 0.40'a göre uyarlandı)
    output_df["Risk_Segmenti"] = pd.cut(
        output_df["Churn_Probability"],
        bins=[0, 0.30, 0.60, 1.0],
        labels=["Düşük Risk", "Orta Risk", "Yüksek Risk"],
        include_lowest=True
    )

    aksiyon_sozlugu = {
        "Yüksek Risk": "Acil Arama ve İkna Teklifi",
        "Orta Risk" : "Hedefli Pazarlama / Çarpraz Satış",
        "Düşük Risk" : "Aksiyon Gerekmez"
    }
    output_df["Onerilen_Aksiyon"] = output_df["Risk_Segmenti"].map(aksiyon_sozlugu)
    output_df["Ana_Risk_Nedeni"] = ana_risk_nedenleri

    final_output_df = output_df.sort_values(by="Churn_Probability", ascending=False)

    # CSV Kayıt
    kayit_yolu = "Musteri_Risk_Cikti_Tablosu_Guncel.csv"
    final_output_df.to_csv(kayit_yolu, index=False)
    print(f"ISLEM TAMAM! Tablo basariyla kaydedildi: {kayit_yolu}")

    
if __name__ == "__main__":
    main()

         
