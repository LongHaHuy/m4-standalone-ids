from datetime import datetime, timezone

# Mẫu FeatureVector chuẩn tương thích M3 (Mục 13 - Bước 6)
SAMPLE_FEATURE_VECTOR = {
    "flow_id": "sim-000001",
    "feature_set_version": "zone05_flow_v1:1.0.0",
    "features": {
        "duration_s": 0.84,
        "total_packets": 18,
        "total_bytes": 9320,
        "src_packet_rate": 12.4,
        "dst_packet_rate": 9.0,
        "byte_rate": 11095.2,
        "mean_packet_bytes": 517.8,
        "packet_ratio": 1.38,
        "byte_ratio": 1.21,
        "dst_port": 443
    },
    "source": "simulator",
    "timestamp": "2026-09-30T13:30:16Z"
}

def make_feature_vector(flow_id: str, row_dict: dict, version: str = "zone05_flow_v1:1.0.0") -> dict:
    """Hàm chuyển đổi 1 dòng dữ liệu thành chuẩn JSON FeatureVector tương thích M3"""
    return {
        "flow_id": flow_id,
        "feature_set_version": version,
        "features": {
            "duration_s": float(row_dict["duration_s"]),
            "total_packets": int(row_dict["total_packets"]),
            "total_bytes": float(row_dict["total_bytes"]),
            "src_packet_rate": float(row_dict["src_packet_rate"]),
            "dst_packet_rate": float(row_dict["dst_packet_rate"]),
            "byte_rate": float(row_dict["byte_rate"]),
            "mean_packet_bytes": float(row_dict["mean_packet_bytes"]),
            "packet_ratio": float(row_dict["packet_ratio"]),
            "byte_ratio": float(row_dict["byte_ratio"]),
            "dst_port": int(row_dict["dst_port"])
        },
        "source": "simulator",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

if __name__ == "__main__":
    import json
    print("--- MẪU FEATURE VECTOR TƯƠNG THÍCH M3 ---")
    print(json.dumps(SAMPLE_FEATURE_VECTOR, indent=2))