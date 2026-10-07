# Hệ thống ML-IDS với dữ liệu mô phỏng (Module 04 Độc lập)

**Cảnh báo:** Toàn bộ kết quả trong dự án này được đánh giá dựa trên SIMULATED DATA (dữ liệu mô phỏng). Kết quả này KHÔNG đại diện cho hiệu năng của hệ thống IDS trên lưu lượng mạng thực tế.

## 1. Giới thiệu
Dự án thực hành triển khai toàn bộ pipeline của một hệ thống Học máy Phát hiện xâm nhập (ML-IDS), bao gồm: sinh dữ liệu mô phỏng, huấn luyện mô hình (Logistic Regression, Random Forest), đóng gói artifact và chạy dịch vụ API suy luận (Inference) không phụ thuộc vào thiết bị mạng thật.

## 2. Cấu trúc mã nguồn
Dự án được chia thành các thư mục độc lập mô phỏng kiến trúc phần mềm thực tế[cite: 13]:
* **`config/feature_set.yaml`**: Định nghĩa và khóa 10 đặc trưng (feature) dữ liệu đầu vào[cite: 13].
* **`simulator/`**: Chứa kịch bản sinh dữ liệu (`generate_dataset.py`) và kịch bản gửi dữ liệu tuần tự (`replay.py`)[cite: 13].
* **`data/`**: Chứa dataset thô `synthetic_ids.csv` và dữ liệu chuỗi `replay.jsonl`[cite: 13].
* **`app/`**: Chứa logic chính gồm huấn luyện (`train.py`), kiểm tra đầu vào (`validator.py`), API suy luận (`main.py`) và đo lường hiệu năng (`evaluate.py`)[cite: 13].
* **`artifacts/model_v1/`**: Nơi lưu giữ mô hình `model.joblib` tốt nhất và siêu dữ liệu `metadata.json`[cite: 13].
* **`Report.ipynb`**: Sổ tay báo cáo kết quả, EDA và minh chứng thực hành[cite: 13].

## 3. Hướng dẫn cài đặt
**Bước 1:** Khởi tạo môi trường ảo[cite: 13]
```bash
python3 -m venv .venv

**Bước 2:** Kích hoạt môi trường và cài đặt thư viện[cite: 13]
# Windows
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

**Bước 3:** Khởi chạy API suy luận[cite: 13]
uvicorn app.main:app --host 127.0.0.1 --port 8004