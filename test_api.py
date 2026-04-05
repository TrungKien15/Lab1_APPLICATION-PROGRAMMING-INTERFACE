import requests

url = "http://127.0.0.1:8000/predict"

data = {"text": "I hate this"}

res = requests.post(url, json=data)

print(res.json())