import requests
import json

url = "http://127.0.0.1:8000/api/adv/move/"
headers = {"Content-Type": "application/json", "Authorization": "Token b95b972e4e3e23509a22a9d5843ce3c7549e42a0"}
payload = {"direction": "n"}

r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.content)