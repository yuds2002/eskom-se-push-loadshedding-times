from datetime import datetime
import requests

url = "https://developer.sepush.co.za/business/2.0/area?id=capetown-5-claremont"

payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}

response = requests.request("GET", url, data=payload, headers=headers)
date= datetime.today().strftime('%Y-%m-%d')
current_time = datetime.today().strftime('%H:%M')

text = response.text

start = text[text.find('"date":'+'"'+date+'"')::]
split = start[:start.find("{")].split(",[")

stage0 = split[0].split("[[")[1] 
split[0] = stage0 

offset = len('note":"Stage ')
stage_begin = text.find('note":"Stage ')+offset
stage = text[stage_begin:stage_begin+1:]
print("Stage: "+stage)


times = []

if (int(stage)+1)<=(len(split)):
    times = split[int(stage)-1]
else:
    times = split[0]

times = times.split('",')

file = open("log.txt","r+")
lines = file.readlines()

print("-------------")
for i in times:
    i = i.replace('"', '')
    i = i.replace(']','')
    
    start_end = i.split("-")
    start_time = start_end[0]
    end_time = start_end[1]
    if current_time < start_time:
        req = 'https://maker.ifttt.com/trigger/recieve_loadshedding_time/with/key/FctvAiSHAmO0BMOKF4YhO?value1='+start_time+'&'+'value2='+end_time
        req_w_date = date+" - "+req
        if req_w_date+"\n" not in lines:
            file.write(req_w_date+'\n')
            print(i+" => request made")
            requests.post(req)
        else:
            print(i+" => already there")
file.close()

print("-------------")

