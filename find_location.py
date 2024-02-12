import requests
import json
area_name = input("What is the name of your area?\n")
esp_token = input("Please input you EskomSePush-API-token:\n")

url     = 'https://developer.sepush.co.za/business/2.0/areas_search?text='+area_name
headers = { 'token' : esp_token }
res = requests.get(url, headers=headers)

out = json.loads(res.text)
print("Name\t\tID")
for area in out["areas"]:
    print(area["name"]+"\t"+area["id"])

