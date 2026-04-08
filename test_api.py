import requests
import json

url = "http://127.0.0.1:8000/predict"

def test(title, data):
    print(f"\n=== {title} ===")
    res = requests.post(url, json=data)
    try:
        print(json.dumps(res.json(), indent=2))
    except:
        print(res.text)


# ===== Test =====

test("Single", {"text": "I love this product"})

test("Multiple", {
    "text": ["I love this", "I hate this", "This is amazing"]
})

test("Invalid number", {"text": "123"})

test("Invalid random", {"text": "asdfgh qwerty"})

test("Invalid short", {"text": "ok"})
