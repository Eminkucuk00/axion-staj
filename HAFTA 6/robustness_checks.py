import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, log_loss, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import warnings

# final_pipeline dosyasındaki veri hazırlama fonksiyonunu çağırıyorum.
from final_pipeline import preprocess_data

warnings.filterwarnings("ignore")

def print_metrics(y_true, y_pred, y_probs, title=""):
    print(f"--- {title} ---")
    print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision : {precision_score(y_true, y_pred):.4f}")
    print(f"Recall : {recall_score(y_true, y_pred):.4f}")
    print(f"F1_Score : {f1_score(y_true, y_pred)}:.4f")
    print(f"log Loss : {log_loss(y_true, y_probs):.4f}")

def main():
    print("Veri Yükleniyor...")
    df_orijinal = pd.read_csv("BankChurners.csv")
    df_hazir = preprocess_data(df_orijinal)

    X = df_hazir.drop(columns=['Gercek_Durum', 'CLIENTNUM'])
    y = df_hazir['Gercek_Durum']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    # 2. OVERFITTING KONTROLÜ
    print("\n" + "="*50)
    print("1. OVERFITTING KONTROLÜ (SMOTE2LU MODEL)")
    print("="*50)
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

    model = XGBClassifier(random_state=42, learning_rate=0.1, max_depth=6, n_estimators=100, eval_metric='logloss')
    model.fit(X_train_smote, y_train_smote)

    # Train Skorları
    y_train_pred = model.predict(X_train_smote)
    y_train_probs = model.predict_proba(X_train_smote)[:, 1]
    print_metrics(y_train_smote, y_train_pred, y_train_probs, "TRAIN SET PERFORMANSI")

    # Test Skorları (0.40)
    y_test_probs = model.predict_proba(X_test_scaled)[:, 1]
    y_test_pred = (y_test_probs >= 0.40).astype(int)
    print_metrics(y_test, y_test_pred, y_test_probs, "TEST SETİ PERFORMANSI")

    # 3. CROSS-VALIDATION
    print("\n" + "="*50)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train_smote, y_train_smote, cv=cv, scoring='accuracy')
    print(f"CV Accuracy Skorları: {cv_scores}")
    print(f"CV Ortalama Acuraccy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})\n")

    # 4. SMOTE ETKİSİ
    print("\n" + "="*50)
    print("3. SMOTE ETKİSİ KONTROLÜ (TEST SETİ ÜZERİNDE)")
    print("="*50)
    #SMOTE OLMADAN Model Eğitimi
    model_no_smote = XGBClassifier(random_state=42, learning_rate=0.1, max_depth=6, n_estimators=100, eval_metric='logloss')
    model_no_smote.fit(X_train_scaled, y_train)
    y_test_probs_no_smote = model_no_smote.predict_proba(X_test_scaled)[:,1]
    y_test_pred_no_smote = (y_test_probs_no_smote >= 0.40).astype(int)

    print(">>> SMOTE YOKKEN (Dengesiz Veri) <<<")
    print(f"Recall (Terk edenleri yakalama): {recall_score(y_test, y_test_pred_no_smote):.4f}")
    print(f"Precision (Yanlış alarm durumu): {precision_score(y_test, y_test_pred_no_smote):.4f}\n")

    print(">>> SMOTE VARKEN (Dengeli Veri) <<<")
    print(f"Recall (Terk edenleri yakalama): {recall_score(y_test, y_test_pred):.4f}")
    print(f"Precision (Yanlış alarm durumu): {precision_score(y_test, y_test_pred):.4f}\n")

    # 5. THRESHOLD ANALİZİ
    print("\n" + "="*50)
    print("4. THRESHOLD (EŞİK DEĞER) ANALİZİ")
    print("="*50)
    esikler = [0.30, 0.40, 0.50, 0.60]
    for esik in esikler:
        y_pred_esik = (y_test_probs >= esik).astype(int)
        r = recall_score(y_test, y_pred_esik)
        p = precision_score(y_test, y_pred_esik)
        f1 = f1_score(y_test, y_pred_esik)

        # Confusion Matrix (TN, FP, FN, TP)
        tn, fp, fn, tp=confusion_matrix(y_test,y_pred_esik).ravel()

        print(f"Threshold = {esik:.2f}")
        print(f"   Metrikler: Recall: {r:.4f} | Precision: {p:.4f} | F1: {f1:.4f}")
        print(f"  Matris    : TP (Doğru Yakalanan): {tp} | FN (Kaçırılan Gidenler): {fn}")
        print(f"              TN (Doğru Kalanlar) : {tn} | FP (Yanlış Alarm)     : {fp}\n" )

if __name__ == "__main__":
    main()


