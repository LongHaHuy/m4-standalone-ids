# Chia tập train/ test
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Đọc dữ liệu từ thư mục data
df = pd.read_csv("data/synthetic_ids.csv")

# 2. Khai báo 10 features khớp chính xác với feature_set.yaml
FEATURES = [
    "duration_s", "total_packets", "total_bytes", 
    "src_packet_rate", "dst_packet_rate", "byte_rate", 
    "mean_packet_bytes", "packet_ratio", "byte_ratio", "dst_port"
]

X = df[FEATURES]
y = df["label"]

# 3. Chia tập Train/Test (Tỷ lệ 75/25)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("--- KẾT QUẢ CHIA TẬP DỮ LIỆU ---")
print(f"Kích thước tập Train (X_train): {X_train.shape}")
print(f"Kích thước tập Test (X_test): {X_test.shape}")

#-------------------------------------
# Huấn luyện loggistic Regression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report, f1_score, matthews_corrcoef

# 1. Huấn luyện Logistic Regression
lr = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, random_state=42))
])

# Fit mô hình vào tập Train
lr.fit(X_train, y_train)

# Dự đoán thử với tập Test
pred_lr = lr.predict(X_test)

# 2. Đánh giá kết quả
print("\n--- KẾT QUẢ HUẤN LUYỆN LOGISTIC REGRESSION ---")
print("Confusion Matrix:")
print(confusion_matrix(y_test, pred_lr, labels=["NORMAL", "SIM_ATTACK"]))
print("\nBáo cáo phân loại (Classification Report):")
print(classification_report(y_test, pred_lr, digits=4))

# Các chỉ số so sánh 
print(f"LR F1 = {f1_score(y_test, pred_lr, pos_label='SIM_ATTACK')}")
print(f"LR MCC= {matthews_corrcoef(y_test, pred_lr)}")


#-------------------------------------
# Huấn luyện Random Forest
from sklearn.ensemble import RandomForestClassifier

# 3. Huấn luyện Random Forest để so sánh
print("\n--- KẾT QUẢ HUẤN LUYỆN RANDOM FOREST ---")
rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, pred_rf, labels=["NORMAL", "SIM_ATTACK"]))

print("\nBáo cáo phân loại (Classification Report) - RF:")
print(classification_report(y_test, pred_rf, digits=4))
      
print(f"RF F1 = {f1_score(y_test, pred_rf, pos_label='SIM_ATTACK')}")
print(f"RF MCC= {matthews_corrcoef(y_test, pred_rf)}")


#-----------------------------------
# Lưu model artifact
import joblib
import json
import hashlib
from pathlib import Path

# 4. Đóng gói mô hình và metadata
p = Path("artifacts/model_v1")
p.mkdir(parents=True, exist_ok=True)

# Lưu file mô hình bằng joblib
joblib.dump(lr, p / "model.joblib")

# Khai báo siêu dữ liệu (metadata)
meta = { 
    "model_id": "ZONE05-STANDALONE-LR", 
    "model_version": "1.0.0-SIM", 
    "feature_set_version": "zone05_flow_v1:1.0.0", 
    "feature_order": FEATURES, 
    "classes": list(lr.classes_), 
    "data_source": "synthetic_ids.csv", 
    "warning": "SIMULATED DATA - NOT REAL NETWORK IDS PERFORMANCE"
}

# Lưu file JSON
(p / "metadata.json").write_text(json.dumps(meta, indent=2))

# In mã băm SHA256 để kiểm tra tính toàn vẹn
print("\n--- KẾT QUẢ ĐÓNG GÓI MÔ HÌNH (ARTIFACTS) ---")
for f in ["model.joblib", "metadata.json"]:
    b = (p / f).read_bytes()
    print(f"{f}: {hashlib.sha256(b).hexdigest()}")



#-----------------------------------
#  Kiểm tra lưu/nạp model
loaded = joblib.load("artifacts/model_v1/model.joblib")
p1 = lr.predict(X_test.iloc[:20])
p2 = loaded.predict(X_test.iloc[:20])

# Kiểm tra điều kiện để in ra báo cáo
assert (p1 == p2).all()
print("PASS: predictions identical")