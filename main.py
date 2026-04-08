from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Union
import re
import time

app = FastAPI()

# ===== Load model =====
classifier = pipeline("sentiment-analysis")

# ===== Input =====
class TextInput(BaseModel):
    text: Union[str, List[str]]


# ===== VALIDATION =====

def is_valid_text(text: str):
    text = text.strip()

    # 1. Không rỗng
    if text == "":
        return False, "Text is empty"

    # 2. Phải có chữ cái
    if not re.search(r"[a-zA-Z]", text):
        return False, "Text must contain alphabet characters"

    # 3. Không phải toàn ký tự lặp (aaaaa, !!!!!)
    if len(set(text)) <= 2:
        return False, "Text looks like repeated characters"

    # 4. Phải có ít nhất 2 từ
    words = text.split()
    if len(words) < 2:
        return False, "Text too short or not meaningful"

    # 5. Không phải kiểu random string (asdfgh qwerty)
    vowel_count = sum(1 for c in text.lower() if c in "aeiou")
    if vowel_count / len(text) < 0.2:
        return False, "Text looks like random characters"

    return True, ""


# ===== API =====

# 1. Root
@app.get("/")
def root():
    return {
        "message": "Sentiment Analysis API",
        "usage": "POST /predict with text input"
    }


# 2. Health
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": classifier is not None
    }


# 3. Predict
@app.post("/predict")
def predict(input: TextInput):
    start_time = time.time()

    # ===== Chuẩn hóa input =====
    if isinstance(input.text, str):
        texts = [input.text]
    elif isinstance(input.text, list):
        texts = input.text
    else:
        raise HTTPException(status_code=400, detail="Invalid input format")

    if len(texts) == 0:
        raise HTTPException(status_code=400, detail="Empty input list")

    # ===== Validate từng câu =====
    for t in texts:
        if not isinstance(t, str):
            raise HTTPException(status_code=400, detail="Each item must be a string")

        valid, message = is_valid_text(t)
        if not valid:
            raise HTTPException(status_code=400, detail=f"Invalid text: '{t}' - {message}")

    # ===== Gọi model =====
    try:
        results = classifier(texts)

        output = []
        for i, r in enumerate(results):
            score = round(r["score"], 4)

            output.append({
                "text": texts[i],
                "label": r["label"],
                "score": score
            })

        return {
            "success": True,
            "count": len(output),
            "processing_time": round(time.time() - start_time, 4),
            "results": output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
