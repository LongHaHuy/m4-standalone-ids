import time
import json
import platform
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

URL = "http://127.0.0.1:8004/api/v1/predict"
META = json.loads(Path("artifacts/model_v1/metadata.json").read_text())

# 1. Chuẩn bị 200 FeatureVectors từ synthetic_ids.csv
df = pd.read_csv("data/synthetic_ids.csv").iloc[:200]
vectors = []
for idx, row in df.iterrows():
    vectors.append({
        "flow_id": f"bench-{idx + 1:06d}",
        "feature_set_version": "zone05_flow_v1:1.0.0",
        "features": {
            "duration_s": float(row["duration_s"]),
            "total_packets": int(row["total_packets"]),
            "total_bytes": float(row["total_bytes"]),
            "src_packet_rate": float(row["src_packet_rate"]),
            "dst_packet_rate": float(row["dst_packet_rate"]),
            "byte_rate": float(row["byte_rate"]),
            "mean_packet_bytes": float(row["mean_packet_bytes"]),
            "packet_ratio": float(row["packet_ratio"]),
            "byte_ratio": float(row["byte_ratio"]),
            "dst_port": int(row["dst_port"])
        },
        "source": "simulator",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    })

# 2. Thực hiện đo Client Latency và Throughput trên 200 requests
print("--- ĐO LƯỜNG LATENCY & THROUGHPUT ---")
times = []
server_inference_ms = []
n_success = 0

t_start = time.perf_counter()
for fv in vectors[:200]:
    t0 = time.perf_counter()
    r = requests.post(URL, json=fv, timeout=2)
    times.append((time.perf_counter() - t0) * 1000)
    if r.status_code == 200:
        n_success += 1
        server_inference_ms.append(r.json()["inference_ms"])
t_measurement = time.perf_counter() - t_start

throughput = n_success / t_measurement

print(f"n = {len(times)} (Success = {n_success})")
print(f"Client Latency -> mean_ms = {np.mean(times):.4f} | median_ms = {np.median(times):.4f} | p95_ms = {np.percentile(times, 95):.4f}")
print(f"Model Inference (in-service) -> mean_ms = {np.mean(server_inference_ms):.4f}")
print(f"T_measurement = {t_measurement:.4f} s")
print(f"Throughput = {throughput:.2f} requests/sec")

print("\n--- THÔNG TIN MÔI TRƯỜNG BÁO CÁO ---")
print(f"Python version: {platform.python_version()}")
print(f"OS / Platform : {platform.system()} {platform.release()} ({platform.machine()})")
print(f"Processor     : {platform.processor()}")
print(f"Model version : {META['model_version']} ({META['model_id']})")



#----------------------------------------------
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, matthews_corrcoef, confusion_matrix
)

# 3. Đánh giá trên test set có nhãn (Mục 19 - Lab 4.8)
print("\n--- ĐÁNH GIÁ TRÊN TEST SET CÓ NHÃN (LAB 4.8) ---")
print(f"Warning            : {META['warning']}")
print(f"Data source        : {META['data_source']}")
print(f"Model version      : {META['model_version']}")
print(f"Feature set version: {META['feature_set_version']}")

df_full = pd.read_csv("data/synthetic_ids.csv")
FEATURES = META["feature_order"]
X = df_full[FEATURES]
y = df_full["label"]

# Tái tạo đúng tập test split (chưa dùng để fit model)
_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = joblib.load("artifacts/model_v1/model.joblib")
pred = model.predict(X_test)

print("Confusion Matrix (NORMAL, SIM_ATTACK):")
print(confusion_matrix(y_test, pred, labels=["NORMAL", "SIM_ATTACK"]))
print("Accuracy =", accuracy_score(y_test, pred))
print("Precision=", precision_score(y_test, pred, pos_label="SIM_ATTACK"))
print("Recall   =", recall_score(y_test, pred, pos_label="SIM_ATTACK"))
print("F1       =", f1_score(y_test, pred, pos_label="SIM_ATTACK"))
print("MCC      =", matthews_corrcoef(y_test, pred))