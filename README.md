# LAB 1 - Xây dựng Web API với FastAPI và Hugging Face

* Họ tên: Trần Trung Kiên
* MSSV: 24120079

---

## Mô hình sử dụng

Trong bài này, em sử dụng mô hình **phân tích cảm xúc (Sentiment Analysis)** từ Hugging Face:

* Tên model: distilbert-base-uncased-finetuned-sst-2-english
* Link: https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english

Mô hình này có khả năng phân loại một đoạn văn bản tiếng Anh thành hai loại:

* **POSITIVE**: cảm xúc tích cực
* **NEGATIVE**: cảm xúc tiêu cực

---

## Mô tả hệ thống

Hệ thống được xây dựng bằng FastAPI, cho phép người dùng gửi dữ liệu văn bản và nhận lại kết quả phân tích cảm xúc từ mô hình Hugging Face.

API bao gồm 3 chức năng chính:

* GET /
  Trả về thông tin giới thiệu về hệ thống

* GET /health
  Kiểm tra trạng thái hoạt động của API

* POST /predict
  Nhận dữ liệu đầu vào và trả về kết quả phân tích cảm xúc

Ngoài ra, hệ thống có kiểm tra dữ liệu đầu vào và xử lý các trường hợp lỗi cơ bản.

---


## Cách chạy chương trình

Bước 1: Clone project
git clone https://github.com/TrungKien15/Lab1_APPLICATION-PROGRAMMING-INTERFACE.git
cd Lab1_APPLICATION-PROGRAMMING-INTERFACE

Bước 2: Tạo môi trường ảo
python -m venv venv

Bước 3: Kích hoạt môi trường
venv\Scripts\activate

Nếu gặp lỗi quyền (Execution Policy), chạy:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate

Bước 4: Cài thư viện
pip install -r requirements.txt

Bước 5: Chạy API
python -m uvicorn main:app --reload
Bước 6: Test API

Mở trình duyệt và truy cập:

http://127.0.0.1:8000/docs

Sau đó có thể test API.



## Cách sử dụng API

### Chức năng: POST /predict

### Dữ liệu đầu vào

API hỗ trợ cả 1 câu và nhiều câu:

```json
{
  "text": "I love this product"
}
```

hoặc

```json
{
  "text": ["I love this product", "I hate this service"]
}
```

---

### Kết quả trả về

```json
{
  "success": true,
  "count": 2,
  "processing_time": 0.12,
  "results": [
    {
      "text": "I love this product", 
      "label": "POSITIVE",
      "score": 0.99
    },
    {
      "text": "I hate this service",
      "label": "NEGATIVE",
      "score": 0.99
    }
  ]
}
```

---

## Kiểm tra API bằng Python

File `test_api.py` sử dụng thư viện `requests` để gửi request đến API:

```python
import requests

url = "http://127.0.0.1:8000/predict"

data = {
    "text": ["I love this", "I hate this"]
}

response = requests.post(url, json=data)
print(response.json())
```

---

## Xử lý lỗi

Hệ thống có kiểm tra một số trường hợp lỗi:

* Dữ liệu đầu vào rỗng
* Sai định dạng (không phải string hoặc list)
* Lỗi trong quá trình gọi mô hình

---

## Video demo

Link video demo:
https://drive.google.com/file/d/1_XKQYAPHPBpXLu5vFZoam-oReptOe2ea/view?usp=sharing

---

