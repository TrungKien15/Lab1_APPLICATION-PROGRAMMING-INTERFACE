# LAB 1 - Xây dựng Web API với FastAPI và Hugging Face

## Thông tin sinh viên

* Họ tên: Trần Trung Kiên
* MSSV: (điền MSSV)

---

## Giới thiệu

Trong bài lab này, em xây dựng một hệ thống Web API sử dụng FastAPI để thực hiện phân tích cảm xúc văn bản.
Hệ thống cho phép người dùng gửi vào một hoặc nhiều câu tiếng Anh, sau đó trả về kết quả phân loại cảm xúc là **POSITIVE** hoặc **NEGATIVE**.

---

## Mô hình sử dụng

Hệ thống sử dụng mô hình từ Hugging Face:

* Tên model: distilbert-base-uncased-finetuned-sst-2-english
* Link: https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english

---

## Công nghệ sử dụng

* FastAPI: xây dựng API
* Uvicorn: chạy server
* Transformers: sử dụng mô hình AI
* Torch: backend cho model
* Requests: test API

---

## Chức năng chính


### 1. GET /

Trả về thông tin giới thiệu về hệ thống.

---

### 2. GET /health

Kiểm tra trạng thái hoạt động của hệ thống.


---

### 3. POST /predict

Phân tích cảm xúc văn bản.



---

## Xử lý dữ liệu đầu vào

Hệ thống có kiểm tra dữ liệu đầu vào nhằm đảm bảo tính hợp lệ:

* Không chấp nhận chuỗi rỗng
* Phải chứa ký tự chữ cái
* Không chấp nhận chuỗi lặp (ví dụ: "aaaaaa")
* Phải có ít nhất 2 từ
* Loại bỏ các chuỗi không có nghĩa (ví dụ: "asdfgh qwerty")

Nếu dữ liệu không hợp lệ, API sẽ trả về lỗi với mã HTTP 400.

---

## Xử lý lỗi

API xử lý các trường hợp lỗi:

* Sai định dạng dữ liệu
* Thiếu dữ liệu
* Dữ liệu không hợp lệ
* Lỗi trong quá trình gọi mô hình

---

## Hướng dẫn cài đặt và chạy chương trình

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

## Kiểm thử API bằng Python

Chạy file test:

```bash
python test_api.py
```

File này sẽ kiểm tra:

* Input hợp lệ
* Input nhiều câu
* Input lỗi

---

## Video demo

(Link video tại đây)




