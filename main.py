from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Union
import time

app = FastAPI()

# Load model
classifier = pipeline("sentiment-analysis")

# ===== Input =====
class TextInput(BaseModel):
    text: Union[str, List[str]]  # cho phép 1 câu hoặc nhiều câu

# ===== API =====

@app.get("/")
def root():
    return {
        "name": "Sentiment Analysis API",
        "description": "Phân tích cảm xúc văn bản (positive/negative)",
        "version": "1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": classifier is not None
    }

@app.post("/predict")
def predict(input: TextInput):
    start_time = time.time()

    # ===== Validate =====
    if isinstance(input.text, str):
        texts = [input.text]
    elif isinstance(input.text, list):
        texts = input.text
    else:
        raise HTTPException(status_code=400, detail="Invalid input format")

    # Check rỗng
    if len(texts) == 0:
        raise HTTPException(status_code=400, detail="Empty input list")

    # Check từng phần tử
    for t in texts:
        if not isinstance(t, str) or t.strip() == "":
            raise HTTPException(status_code=400, detail="Invalid text in list")

    try:
        results = classifier(texts)

        response = []
        for i, r in enumerate(results):
            response.append({
                "text": texts[i],
                "label": r["label"],
                "score": round(r["score"], 4)
            })

        end_time = time.time()

        return {
            "success": True,
            "count": len(response),
            "processing_time": round(end_time - start_time, 4),
            "results": response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference error: {str(e)}"
        )