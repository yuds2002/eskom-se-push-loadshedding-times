import requests


payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}

url = "https://developer.sepush.co.za/business/2.0/api_allowance"
response = requests.request("GET", url, headers=headers, data=payload)
text = response.text

out = text[text.find("count"):text.find('"t')]
out = out.replace('"','').replace(",",' ')
count = out[out.find(":")+1:out.find(" ")]
print(count+"/50")