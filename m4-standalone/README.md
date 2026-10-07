# Hệ thống ML-IDS: Xây dựng Pipeline Học máy Phát hiện Xâm nhập (Module 04)

> **⚠️ CẢNH BÁO QUAN TRỌNG:** Toàn bộ dữ liệu, mô hình và các chỉ số đo lường hiệu năng (Latency, Throughput, F1-score, MCC) trong dự án này được thực hiện dựa trên **Dữ liệu mô phỏng**. Kết quả này hoàn toàn KHÔNG đại diện cho hiệu năng thực tế của một hệ thống NIDS (Network Intrusion Detection System) trên lưu lượng mạng thật[cite: 17].

## 1. Tổng quan Dự án
Dự án này triển khai kiến trúc phần mềm độc lập cho hệ thống Machine Learning - Intrusion Detection System (ML-IDS)[cite: 17]. Mục tiêu cốt lõi là xây dựng hoàn chỉnh một pipeline học máy bao gồm:
- Sinh dữ liệu mô phỏng theo hợp đồng dữ liệu (Data Contract) quy định trước[cite: 17].
- Phân tích EDA, tiền xử lý và chia tách tập dữ liệu (Train/Test Split)[cite: 17].
- Huấn luyện và so sánh mô hình **Logistic Regression (LR)** và **Random Forest (RF)**[cite: 17].
- Đóng gói (Serialization) mô hình và siêu dữ liệu (Metadata) dưới dạng Artifact[cite: 17].
- Triển khai **Inference API** độc lập xử lý dự đoán thời gian thực qua giao thức HTTP[cite: 17].
- Kiểm thử độ vững chãi của hệ thống với các dữ liệu đầu vào lỗi (Fault Tolerance) và kiểm thử phát lại luồng dữ liệu (Data Replay)[cite: 14, 17].

## 2. Cấu trúc Mã nguồn (Project Structure)
Dự án được phân rã thành các module chức năng độc lập nhằm đảm bảo khả năng bảo trì và dễ dàng tích hợp vào hệ thống thật (Zone 05)[cite: 17]:

```text
m4-standalone/
├── app/                      # Mã nguồn lõi (Core Application)
│   ├── main.py               # Khởi chạy dịch vụ FastAPI (Inference API)[cite: 14, 17]
│   ├── train.py              # Logic huấn luyện, đánh giá và lưu Artifact[cite: 14, 17]
│   ├── validator.py          # Bộ lọc kiểm tra tính hợp lệ của FeatureVector[cite: 14, 17]
│   ├── evaluate.py           # Script đo lường Runtime (Latency/Throughput)[cite: 14, 17]
│   ├── inference.py          # Kịch bản kiểm thử lỗi đầu vào (Fault test E1-E5)[cite: 17]
│   └── schemas.py            # Định nghĩa cấu trúc dữ liệu Pydantic[cite: 17]
├── simulator/                # Công cụ mô phỏng[cite: 14]
│   ├── generate_dataset.py   # Script sinh dataset ngẫu nhiên (NORMAL & SIM_ATTACK)[cite: 14, 17]
│   └── replay.py             # Script phát lại dữ liệu tuần tự vào API[cite: 14, 17]
├── config/                   # Cấu hình tĩnh
│   └── feature_set.yaml      # Khóa hợp đồng dữ liệu (10 features chuẩn)[cite: 14, 17]
├── data/                     # Dữ liệu cục bộ
│   ├── synthetic_ids.csv     # Dataset thô (2000 mẫu)[cite: 14, 17]
│   └── replay.jsonl          # Dữ liệu Replay định dạng JSONL[cite: 14, 17]
├── artifacts/model_v1/       # Nơi lưu trữ Model Registry
│   ├── model.joblib          # Trọng số mô hình đã huấn luyện[cite: 14, 17]
│   └── metadata.json         # Siêu dữ liệu mô hình và cảnh báo[cite: 14, 17]
├── results/                  # Kết quả truy xuất
│   └── predictions.jsonl     # Log phản hồi từ API sau quá trình Replay[cite: 17]
├── requirements.txt          # Danh sách thư viện phụ thuộc[cite: 14]
└── Report.ipynb              # Sổ tay báo cáo kết quả, đồ thị EDA và minh chứng[cite: 14]
```
### 3. Hướng dẫn Cài đặt và Vận hành (Quick Start)

#### 3.1. Thiết lập Môi trường
Dự án yêu cầu Python 3.10 trở lên[cite: 17].

```bash
# 1. Khởi tạo môi trường ảo[cite: 17]
python3 -m venv .venv

# 2. Kích hoạt môi trường[cite: 17]
# Trên Windows:
.\.venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source .venv/bin/activate

# 3. Cài đặt các thư viện lõi[cite: 17]
pip install -r requirements.txt
``` 

#### 3.2. Khởi chạy Dịch vụ API
Khởi chạy tiến trình Inference API (lắng nghe tại cổng 8004)[cite: 17]:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8004
```
Kiểm tra trạng thái (Health Check) của dịch vụ[cite: 17]:
```bash
curl [http://127.0.0.1:8004/api/v1/health](http://127.0.0.1:8004/api/v1/health)
```
### 3.3. Kiểm thử Replay và Fault Test
Mở một cửa sổ Terminal mới (đảm bảo đã kích hoạt .venv) để gửi dữ liệu mô phỏng [cite: 17]:
```bash
# Gửi tuần tự 50 vector để kiểm tra hệ thống[cite: 17]
python simulator/replay.py

# Đo lường Latency và Throughput của dịch vụ[cite: 17]
python app/evaluate.py
```

## 4. Tiêu chí Đánh giá và Minh chứng (PASS Criteria)
Dự án đã vượt qua toàn bộ các bài kiểm thử khắt khe của Module 04 theo Phụ lục A[cite: 17]:

* 1. Dữ liệu & EDA: Dataset 2000 mẫu được sinh thành công (lưu seed), không chứa giá trị NaN/Inf dị thường[cite: 17].

* 2. Train/Test Split: Đảm bảo nguyên tắc bảo mật dữ liệu, không có data leakage trong quá trình fit Scaler[cite: 17].

* 3. Huấn luyện Mô hình: Pipeline Logistic Regression và Random Forest được đánh giá chi tiết qua F1-score và MCC[cite: 17].

* 4. Artifact Management: Quản lý thành công file .joblib và metadata.json chứa mã băm (checksum) và phiên bản 1.0.0-SIM[cite: 17].

* 5. Độ vững chãi (Fault Tolerance): Bộ Validator chặn đứng hoàn toàn 4 ca kiểm thử dị biệt (E1-E4) bằng mã HTTP 422, đảm bảo tiến trình API không bị sập (E5 trả HTTP 200)[cite: 17].

* 4. Đo lường Hiệu năng: Ghi nhận đầy đủ thông số Throughput (requests/sec) và Latency (mean, median, p95) ở Runtime[cite: 17].

*Ghi chú: Báo cáo đồ thị trực quan, phân tích dữ liệu chuyên sâu và toàn bộ ảnh chụp minh chứng thực thi (Evidence) được đính kèm chi tiết trong file Report.ipynb*[cite: 14].