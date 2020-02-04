import requests
import json

url = "http://127.0.0.1:8000/api/adv/move/"
headers = {"Content-Type": "application/json", "Authorization": "Token 20df5ee236a10d07628f7cf5c6d4dec07db941d9"}
payload = {"direction": "n"}


r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.content)