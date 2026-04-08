from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Union
import time
import re
import logging
from datetime import datetime

# ===== Khởi tạo app =====
app = FastAPI()

# ===== Logging (ghi log khi có request) =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Load model Hugging Face =====
classifier = pipeline("sentiment-analysis")

# ===== Input schema =====
class TextInput(BaseModel):
    text: Union[str, List[str]]  # hỗ trợ 1 câu hoặc nhiều câu


# ===== Danh sách từ phổ biến (để kiểm tra câu có nghĩa) =====
COMMON_WORDS = {
    "i", "you", "this", "that", "is", "are", "am",
    "love", "hate", "good", "bad", "product", "service",
    "it", "very", "really", "not"
}


# ===== Hàm kiểm tra câu có nghĩa =====
def is_meaningful_text(text: str):
    text = text.lower()

    # phải có ít nhất 1 chữ cái
    if not re.search(r"[a-zA-Z]", text):
        return False

    words = text.split()

    # phải có ít nhất 2 từ
    if len(words) < 2:
        return False

    # phải chứa ít nhất 1 từ phổ biến
    if not any(word in COMMON_WORDS for word in words):
        return False

    return True


# ===== Hàm đánh giá độ tin cậy =====
def get_confidence(score):
    if score > 0.9:
        return "HIGH"
    elif score > 0.7:
        return "MEDIUM"
    else:
        return "LOW"


# ================= API =================

# ===== 1. Trang chủ =====
@app.get("/")
def root():
    return {
        "name": "Sentiment Analysis API",
        "description": "API phân tích cảm xúc văn bản sử dụng Hugging Face",
    }


# ===== 2. Kiểm tra trạng thái =====
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": classifier is not None,
        "time": datetime.now().isoformat()
    }


# ===== 3. Thông tin model =====
@app.get("/model-info")
def model_info():
    return {
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
        "task": "sentiment analysis",
        "labels": ["POSITIVE", "NEGATIVE"]
    }


# ===== 4. API chính =====
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

    # ===== Validate =====
    if len(texts) == 0:
        raise HTTPException(status_code=400, detail="Empty input")

    for t in texts:
        if not isinstance(t, str) or t.strip() == "":
            raise HTTPException(status_code=400, detail="Text is empty")

        if len(t) > 500:
            raise HTTPException(status_code=400, detail="Text too long")

        if not is_meaningful_text(t):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or meaningless text: '{t}'"
            )

    # ===== Log input =====
    logger.info(f"Received input: {texts}")

    # ===== Gọi model =====
    try:
        results = classifier(texts)

        output = []
        for i, r in enumerate(results):
            score = round(r["score"], 4)

            output.append({
                "text": texts[i],
                "label": r["label"],
                "score": score,
                "confidence": get_confidence(score)
            })

        end_time = time.time()

        return {
            "success": True,
            "count": len(output),
            "processing_time": round(end_time - start_time, 4),
            "timestamp": datetime.now().isoformat(),
            "results": output
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=f"Model inference error: {str(e)}"
        )


# ===== 5. API đơn giản (bonus) =====
@app.post("/predict/simple")
def predict_simple(input: TextInput):
    if isinstance(input.text, str):
        texts = [input.text]
    else:
        texts = input.text

    try:
        results = classifier(texts)
        return {
            "results": [r["label"] for r in results]
        }
    except:
        raise HTTPException(status_code=500, detail="Error processing request")
