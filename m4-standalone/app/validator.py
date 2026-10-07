import numpy as np

def validate(fv, meta):
    if fv["feature_set_version"] != meta["feature_set_version"]:
        raise ValueError("FEATURE_SET_VERSION_MISMATCH")
    fs = fv["features"]
    missing = [k for k in meta["feature_order"] if k not in fs]
    if missing:
        raise ValueError(f"MISSING_FEATURES:{missing}")
    x = np.array([float(fs[k]) for k in meta["feature_order"]])
    if not np.isfinite(x).all():
        raise ValueError("NON_FINITE_FEATURE")
    if not 0 <= float(fs["dst_port"]) <= 65535:
        raise ValueError("INVALID_DST_PORT")
    return x.reshape(1, -1)

if __name__ == "__main__":
    import json
    from pathlib import Path
    from schemas import SAMPLE_FEATURE_VECTOR

    meta = json.loads(Path("artifacts/model_v1/metadata.json").read_text())
    x_valid = validate(SAMPLE_FEATURE_VECTOR, meta)
    print("PASS Validator! Kích thước mảng đầu ra:", x_valid.shape)
    print("Mảng dữ liệu:", x_valid)