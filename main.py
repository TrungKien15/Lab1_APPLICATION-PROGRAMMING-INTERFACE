from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Union
import time

app = FastAPI()

# Load model
classifier = pipeline("sentiment-analysis")

# Input schema 
class TextInput(BaseModel):
    text: Union[str, List[str]]  # hỗ trợ 1 câu hoặc nhiều câu


# Hàm kiểm tra text hợp lệ 
def is_valid_text(text: str):
    # phải có ít nhất 1 chữ cái
    return any(c.isalpha() for c in text)


# API

@app.get("/")
def root():
    return {
        "name": "Sentiment Analysis API",
        "description": "Phân tích cảm xúc văn bản (positive/negative)",
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

    # Chuẩn hóa input
    if isinstance(input.text, str):
        texts = [input.text]
    elif isinstance(input.text, list):
        texts = input.text
    else:
        raise HTTPException(status_code=400, detail="Invalid input format")

    #  Validate 
    if len(texts) == 0:
        raise HTTPException(status_code=400, detail="Empty input")

    for t in texts:
        if not isinstance(t, str) or t.strip() == "":
            raise HTTPException(status_code=400, detail="Text is empty")

        if not is_valid_text(t):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid text: '{t}' must contain alphabet characters"
            )

        if len(t.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail=f"Text too short: '{t}'"
            )

    #  Gọi model 
    try:
        results = classifier(texts)

        output = []
        for i, r in enumerate(results):
            output.append({
                "text": texts[i],
                "label": r["label"],
                "score": round(r["score"], 4)
            })

        end_time = time.time()

        return {
            "success": True,
            "count": len(output),
            "processing_time": round(end_time - start_time, 4),
            "results": output
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference error: {str(e)}"
        )
