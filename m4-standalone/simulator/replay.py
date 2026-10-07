import json
import time
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

URL = "http://127.0.0.1:8004/api/v1/predict"
REPLAY_PATH = Path("data/replay.jsonl")
PRED_PATH = Path("results/predictions.jsonl")

# Đảm bảo thư mục tồn tại
REPLAY_PATH.parent.mkdir(parents=True, exist_ok=True)
PRED_PATH.parent.mkdir(parents=True, exist_ok=True)

# Bước 1 & 2: Tạo 50 FeatureVector JSONL từ synthetic_ids.csv với flow_id sim-000001...sim-000050
df = pd.read_csv("data/synthetic_ids.csv").iloc[:50]
sent_ids = []

with open(REPLAY_PATH, "w", encoding="utf-8") as f:
    for idx, row in df.iterrows():
        flow_id = f"sim-{idx + 1:06d}"
        sent_ids.append(flow_id)
        fv = {
            "flow_id": flow_id,
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
        }
        f.write(json.dumps(fv) + "\n")

print(f"Đã tạo {len(sent_ids)} FeatureVector tại {REPLAY_PATH}")
print("--- BẮT ĐẦU REPLAY (1 vector/s) ---")

# Bước 3 & 4: Replay 1 vector/s và lưu Prediction JSONL
received_ids = []
status_codes = []

with open(REPLAY_PATH, "r", encoding="utf-8") as f_in, \
     open(PRED_PATH, "w", encoding="utf-8") as f_out:
    for line in f_in:
        fv = json.loads(line)
        r = requests.post(URL, json=fv, timeout=2)
        res_json = r.json()
        print(r.status_code, res_json)
        
        status_codes.append(r.status_code)
        if r.status_code == 200 and "flow_id" in res_json:
            received_ids.append(res_json["flow_id"])
            f_out.write(json.dumps(res_json) + "\n")
            
        time.sleep(1.0)

# Bước 5: Kiểm tra không mất flow_id và đủ 50 response hợp lệ
print("\n--- KẾT QUẢ KIỂM TRA REPLAY ---")
print(f"Số vector gửi đi: {len(sent_ids)}")
print(f"Số response HTTP 200 nhận về: {status_codes.count(200)}")
assert len(sent_ids) == 50 and sent_ids == received_ids, "FAIL: Mất hoặc lệch flow_id!"
print("PASS: 50 input tạo 50 response hợp lệ, không mất flow_id nào!")