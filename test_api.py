import requests
import json

BASE_URL = "http://127.0.0.1:8000"


# ===== Test GET / =====
def test_root():
    res = requests.get(f"{BASE_URL}/")
    print_response("GET /", res)


# ===== Test GET /health =====
def test_health():
    res = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", res)


# ===== Test GET /model-info =====
def test_model_info():
    res = requests.get(f"{BASE_URL}/model-info")
    print_response("GET /model-info", res)


# ===== Test POST /predict (1 câu) =====
def test_single():
    data = {"text": "I love this product"}
    res = requests.post(f"{BASE_URL}/predict", json=data)
    print_response("POST /predict - Single", res)


# ===== Test POST /predict (nhiều câu) =====
def test_multiple():
    data = {
        "text": [
            "I love this product",
            "I hate this service",
            "This is amazing"
        ]
    }
    res = requests.post(f"{BASE_URL}/predict", json=data)
    print_response("POST /predict - Multiple", res)


# ===== Test POST /predict/simple =====
def test_simple():
    data = {"text": ["I love this", "I hate this"]}
    res = requests.post(f"{BASE_URL}/predict/simple", json=data)
    print_response("POST /predict/simple", res)


# ===== Test input lỗi =====
def test_invalid():
    data = {"text": "123"}
    res = requests.post(f"{BASE_URL}/predict", json=data)
    print_response("POST /predict - Invalid", res)


# ===== MAIN =====
if __name__ == "__main__":
    print("Running API tests...")

    test_root()
    test_health()
    test_model_info()
    test_single()
    test_multiple()
    test_simple()
    test_invalid()

    print("\nDone.")
