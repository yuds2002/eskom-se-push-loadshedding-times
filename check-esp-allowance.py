import requests

url = "https://developer.sepush.co.za/business/2.0/api_allowance"
payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}

response = requests.request("GET", url, headers=headers, data=payload)
text = response.text

out = text[text.find("count"):text.find('"t')]
out = out.replace('"','').replace(",",' ')
print(out)

