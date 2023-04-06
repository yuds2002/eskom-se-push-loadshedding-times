from datetime import datetime
import requests

url = "https://developer.sepush.co.za/business/2.0/area?id=capetown-5-claremont&test=current"
payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}

response = requests.request("GET", url, data=payload, headers=headers)
date= datetime.today().strftime('%Y-%m-%d')

current_time = datetime.today().strftime('%H:%M:%S')


text = response.text

offset = len('note":"Stage ')

stage_begin = text.find('note":"Stage ')+offset

stage = text[stage_begin:stage_begin+1:]

start = text[text.find('"date":'+'"'+date+'"')::]
split = start[:start.find("{")].split(",[")

print("Stage: "+stage)



next = ""
next_start = ""
times = ""
if (int(stage)+1)<=(len(split)):
    times = split[int(stage)-1]
else:
    times = split[1]


print("--------")
print(times[:-1:])
print("--------")


if ',' in times:
    times = times.split(",")
    for time in times:
        time = time.replace('"', '')
        if ']' in time:
            time = time.replace(']','')
        #print(time)
        start_time = time.split('-')[0]
        #print(start_time)
        if start_time > current_time:
            print("Loadshedding at: "+start_time)

            break
else:
    next = times.replace('"','')[:-1:].split("-")
    next_start = next[0]
    next_end = next[1]
    print("Loadshedding at: "+next_start)
