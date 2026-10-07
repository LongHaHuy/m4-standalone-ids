import copy
import json
import numpy as np
import requests
from pathlib import Path
from app.schemas import SAMPLE_FEATURE_VECTOR
from app.validator import validate

URL = "http://127.0.0.1:8004/api/v1/predict"
META = json.loads(Path("artifacts/model_v1/metadata.json").read_text())

print("--- BẮT ĐẦU KIỂM THỬ LỖI ĐẦU VÀO (LAB 4.6: E1 - E5) ---")

# E1: Sai feature_set_version -> Expected: HTTP 422
fv_e1 = copy.deepcopy(SAMPLE_FEATURE_VECTOR)
fv_e1["feature_set_version"] = "zone05_flow_v1:9.9.9"
r1 = requests.post(URL, json=fv_e1, timeout=2)
print(f"E1 (Sai feature_set_version) -> Status: {r1.status_code} | Detail: {r1.json()}")
assert r1.status_code == 422

# E2: Thiếu total_bytes -> Expected: HTTP 422
fv_e2 = copy.deepcopy(SAMPLE_FEATURE_VECTOR)
del fv_e2["features"]["total_bytes"]
r2 = requests.post(URL, json=fv_e2, timeout=2)
print(f"E2 (Thiếu total_bytes)       -> Status: {r2.status_code} | Detail: {r2.json()}")
assert r2.status_code == 422

# E3: NaN/Inf qua unit test -> Expected: Reject (ValueError: NON_FINITE_FEATURE)
fv_e3 = copy.deepcopy(SAMPLE_FEATURE_VECTOR)
fv_e3["features"]["byte_rate"] = float("nan")
try:
    validate(fv_e3, META)
    raise AssertionError("FAIL: E3 không bị chặn!")
except ValueError as e:
    print(f"E3 (NaN/Inf qua unit test)   -> Status: REJECTED | Detail: {e}")

# E4: dst_port > 65535 -> Expected: Reject (HTTP 422)
fv_e4 = copy.deepcopy(SAMPLE_FEATURE_VECTOR)
fv_e4["features"]["dst_port"] = 70000
r4 = requests.post(URL, json=fv_e4, timeout=2)
print(f"E4 (dst_port > 65535)        -> Status: {r4.status_code} (REJECTED) | Detail: {r4.json()}")
assert r4.status_code == 422

# E5: flow_id hợp lệ, vector đúng -> Expected: HTTP 200
fv_e5 = copy.deepcopy(SAMPLE_FEATURE_VECTOR)
r5 = requests.post(URL, json=fv_e5, timeout=2)
print(f"E5 (Vector hợp lệ sau lỗi)   -> Status: {r5.status_code} | Prediction: {r5.json()}")
assert r5.status_code == 200

print("\nPASS: Toàn bộ request lỗi (E1-E4) đã bị chặn, service vẫn hoạt động tốt ở E5!")