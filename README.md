# LAB 1 - Xây dựng Web API với FastAPI và Hugging Face

## Thông tin sinh viên

* Họ tên: Trần Trung Kiên
* MSSV: 24120079

---

## Mô hình sử dụng

Bài lab sử dụng mô hình phân tích cảm xúc từ Hugging Face:

* Tên model: distilbert-base-uncased-finetuned-sst-2-english
* Link: https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english

Mô hình có nhiệm vụ phân loại văn bản tiếng Anh thành:

* POSITIVE (tích cực)
* NEGATIVE (tiêu cực)

---

## Mô tả hệ thống

Hệ thống được xây dựng bằng FastAPI, cung cấp các API để phân tích cảm xúc văn bản.

Các endpoint chính:

* GET /: thông tin hệ thống
* GET /health: kiểm tra trạng thái API
* GET /model-info: thông tin về mô hình
* POST /predict: phân tích cảm xúc (đầy đủ)
* POST /predict/simple: trả về kết quả đơn giản

---

## Đặc điểm nổi bật

* Hỗ trợ cả **một câu hoặc nhiều câu**
* Có **kiểm tra dữ liệu đầu vào**
* Loại bỏ các câu không có nghĩa (ví dụ: "abc", "123")
* Trả về kết quả có cấu trúc rõ ràng
* Có đánh giá **độ tin cậy (confidence)**
* Có xử lý lỗi và logging

---

## Hướng dẫn chạy chương trình

### Bước 1: Clone project

```bash
git clone <link repo>
cd lab1_api
```

---

### Bước 2: Tạo môi trường ảo

```bash
python -m venv venv
```

---

### Bước 3: Kích hoạt môi trường

Windows:

```bash
venv\Scripts\activate
```

Nếu gặp lỗi quyền:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
```

---

### Bước 4: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

### Bước 5: Chạy API

```bash
python -m uvicorn main:app --reload
```

---

### Bước 6: Test API

Truy cập:

http://127.0.0.1:8000/docs

---

## Ví dụ sử dụng

### Input:

```json
{
  "text": ["I love this product", "I hate this service"]
}
```

### Output:

```json
{
  "success": true,
  "count": 2,
  "results": [
    {
      "text": "I love this product",
      "label": "POSITIVE",
      "score": 0.99,
      "confidence": "HIGH"
    },
    {
      "text": "I hate this service",
      "label": "NEGATIVE",
      "score": 0.99,
      "confidence": "HIGH"
    }
  ]
}
```

---

## Kiểm tra bằng Python

Chạy file:

```bash
python test_api.py
```

---

## Xử lý lỗi

API xử lý các trường hợp:

* Input rỗng
* Sai định dạng
* Câu không có nghĩa
* Lỗi khi gọi mô hình

---

## Video demo

(Link video tại đây)

---


