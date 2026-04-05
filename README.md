# LAB 1 - Xây dựng Web API với FastAPI và Hugging Face

## Thông tin sinh viên

* Họ tên: Trần Trung Kiên
* MSSV: (điền MSSV của bạn)

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

## Cài đặt thư viện

Cài đặt các thư viện cần thiết bằng cách mở terminal và nhập lệnh:


pip install -r requirements.txt


---

## Cách chạy chương trình

Chạy API bằng lệnh:

uvicorn main:app --reload

Sau khi chạy, truy cập vào:

http://127.0.0.1:8000/docs

để test API trực tiếp.



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

Các lỗi sẽ được trả về với mã HTTP phù hợp (400 hoặc 500).

---

## Video demo

Link video demo:


---

