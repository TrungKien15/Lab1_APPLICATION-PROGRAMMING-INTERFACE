import requests

url = "http://127.0.0.1:8000/predict"

# ===== Test 1: 1 câu =====
data_single = {
    "text": "I hate this"
}

res1 = requests.post(url, json=data_single)
print("=== Test 1: Single text ===")
print(res1.json())


# ===== Test 2: nhiều câu =====
data_multiple = {
    "text": ["I love this", "I hate this", "This is amazing"]
}

res2 = requests.post(url, json=data_multiple)
print("\n=== Test 2: Multiple texts ===")
print(res2.json())


# ===== Test 3: input lỗi =====
data_invalid = {
    "text": "123"
}

res3 = requests.post(url, json=data_invalid)
print("\n=== Test 3: Invalid input ===")
print(res3.json())
