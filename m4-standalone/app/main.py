from fastapi import FastAPI, HTTPException
import joblib, json, time
from pathlib import Path
from app.validator import validate

ART = Path("artifacts/model_v1")
MODEL = joblib.load(ART / "model.joblib")
META = json.loads((ART / "metadata.json").read_text())

app = FastAPI(title="Zone05 Standalone ML-IDS")

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "model_id": META["model_id"]}

@app.get("/api/v1/model/info")
def info():
    return META

@app.post("/api/v1/predict")
def predict(fv: dict):
    try:
        x = validate(fv, META)
        t0 = time.perf_counter()
        label = MODEL.predict(x)[0]
        prob = MODEL.predict_proba(x)[0]
        dt = (time.perf_counter() - t0) * 1000
        idx = list(MODEL.classes_).index(label)
        return {
            "flow_id": fv["flow_id"],
            "model_id": META["model_id"],
            "model_version": META["model_version"],
            "feature_set_version": META["feature_set_version"],
            "label": str(label),
            "confidence": float(prob[idx]),
            "inference_ms": dt
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))