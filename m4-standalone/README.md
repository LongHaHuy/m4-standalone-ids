# Hệ thống ML-IDS: Xây dựng Pipeline Học máy Phát hiện Xâm nhập (Module 04)

> **⚠️ CẢNH BÁO QUAN TRỌNG:** Toàn bộ dữ liệu, mô hình và các chỉ số đo lường hiệu năng (Latency, Throughput, F1-score, MCC) trong dự án này được thực hiện dựa trên **Dữ liệu mô phỏng**. Kết quả này hoàn toàn KHÔNG đại diện cho hiệu năng thực tế của một hệ thống NIDS (Network Intrusion Detection System) trên lưu lượng mạng thật

## 1. Tổng quan Dự án
Dự án này triển khai kiến trúc phần mềm độc lập cho hệ thống Machine Learning - Intrusion Detection System (ML-IDS). Mục tiêu cốt lõi là xây dựng hoàn chỉnh một pipeline học máy bao gồm:
- Sinh dữ liệu mô phỏng theo hợp đồng dữ liệu (Data Contract) quy định trước
- Phân tích EDA, tiền xử lý và chia tách tập dữ liệu (Train/Test Split).
- Huấn luyện và so sánh mô hình **Logistic Regression (LR)** và **Random Forest (RF)**
- Đóng gói (Serialization) mô hình và siêu dữ liệu (Metadata) dưới dạng Artifact.
- Triển khai **Inference API** độc lập xử lý dự đoán thời gian thực qua giao thức HTTP.
- Kiểm thử độ vững chãi của hệ thống với các dữ liệu đầu vào lỗi (Fault Tolerance) và kiểm thử phát lại luồng dữ liệu (Data Replay).

## 2. Cấu trúc Mã nguồn (Project Structure)
Dự án được phân rã thành các module chức năng độc lập nhằm đảm bảo khả năng bảo trì và dễ dàng tích hợp vào hệ thống thật (Zone 05):

```text
m4-standalone/
├── app/                      # Mã nguồn lõi (Core Application)
│   ├── main.py               # Khởi chạy dịch vụ FastAPI (Inference API)
│   ├── train.py              # Logic huấn luyện, đánh giá và lưu Artifact
│   ├── validator.py          # Bộ lọc kiểm tra tính hợp lệ của FeatureVector
│   ├── evaluate.py           # Script đo lường Runtime (Latency/Throughput)
│   ├── inference.py          # Kịch bản kiểm thử lỗi đầu vào (Fault test E1-E5)
│   └── schemas.py            # Định nghĩa cấu trúc dữ liệu Pydantic
├── simulator/                # Công cụ mô phỏng
│   ├── generate_dataset.py   # Script sinh dataset ngẫu nhiên (NORMAL & SIM_ATTACK)
│   └── replay.py             # Script phát lại dữ liệu tuần tự vào API
├── config/                   # Cấu hình tĩnh
│   └── feature_set.yaml      # Khóa hợp đồng dữ liệu (10 features chuẩn)
├── data/                     # Dữ liệu cục bộ
│   ├── synthetic_ids.csv     # Dataset thô (2000 mẫu)
│   └── replay.jsonl          # Dữ liệu Replay định dạng JSONL
├── artifacts/model_v1/       # Nơi lưu trữ Model Registry
│   ├── model.joblib          # Trọng số mô hình đã huấn luyện
│   └── metadata.json         # Siêu dữ liệu mô hình và cảnh báo
├── results/                  # Kết quả truy xuất
│   └── predictions.jsonl     # Log phản hồi từ API sau quá trình Replay
├── requirements.txt          # Danh sách thư viện phụ thuộc        
└── Report.ipynb              # Sổ tay báo cáo kết quả, đồ thị EDA và minh chứng
```
### 3. Hướng dẫn Cài đặt và Vận hành (Quick Start)

#### 3.1. Thiết lập Môi trường
Dự án yêu cầu Python 3.10 trở lên.

```bash
# 1. Khởi tạo môi trường ảo
python3 -m venv .venv

# 2. Kích hoạt môi trường
# Trên Windows:
.\.venv\Scripts\Activate.ps1
# Trên Linux/macOS:
source .venv/bin/activate

# 3. Cài đặt các thư viện lõi
pip install -r requirements.txt
``` 

#### 3.2. Khởi chạy Dịch vụ API
Khởi chạy tiến trình Inference API (lắng nghe tại cổng 8004):
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8004
```
Kiểm tra trạng thái (Health Check) của dịch vụ:
```bash
curl [http://127.0.0.1:8004/api/v1/health](http://127.0.0.1:8004/api/v1/health)
```
### 3.3. Kiểm thử Replay và Fault Test
Mở một cửa sổ Terminal mới (đảm bảo đã kích hoạt .venv) để gửi dữ liệu mô phỏng :
```bash
# Gửi tuần tự 50 vector để kiểm tra hệ thống
python simulator/replay.py

# Đo lường Latency và Throughput của dịch vụ
python app/evaluate.py
```

## 4. Tiêu chí Đánh giá và Minh chứng (PASS Criteria)
Dự án đã vượt qua toàn bộ các bài kiểm thử khắt khe của Module 04 theo Phụ lục A:

* 1. Dữ liệu & EDA: Dataset 2000 mẫu được sinh thành công (lưu seed), không chứa giá trị NaN/Inf dị thường.

* 2. Train/Test Split: Đảm bảo nguyên tắc bảo mật dữ liệu, không có data leakage trong quá trình fit Scaler.

* 3. Huấn luyện Mô hình: Pipeline Logistic Regression và Random Forest được đánh giá chi tiết qua F1-score và MCC.

* 4. Artifact Management: Quản lý thành công file .joblib và metadata.json chứa mã băm (checksum) và phiên bản 1.0.0-SIM.

* 5. Độ vững chãi (Fault Tolerance): Bộ Validator chặn đứng hoàn toàn 4 ca kiểm thử dị biệt (E1-E4) bằng mã HTTP 422, đảm bảo tiến trình API không bị sập (E5 trả HTTP 200).

* 4. Đo lường Hiệu năng: Ghi nhận đầy đủ thông số Throughput (requests/sec) và Latency (mean, median, p95) ở Runtime.

*Ghi chú: Báo cáo đồ thị trực quan, phân tích dữ liệu chuyên sâu và toàn bộ ảnh chụp minh chứng thực thi (Evidence) được đính kèm chi tiết trong file Report.ipynb*.
