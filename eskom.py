from datetime import datetime
import requests
import json

############
# Input
area_id = "" # eskom area id, please see docs NOTE the string must be lowercase
ifttt_key = "" # ifttt webhook key
file_location = "" # folder location of log file
esp_token = "" # EskomSePush API Token
############

payload = {}
headers = {"token" : esp_token}
date= datetime.today().strftime('%Y-%m-%d')

url = "https://developer.sepush.co.za/business/2.0/api_allowance"
response = requests.request("GET", url, headers=headers, data=payload)
text = json.loads(response.text)
count = int(text["allowance"]["count"])

current_time = datetime.today().strftime('%H:%M')

if count < 50:
    url = "https://developer.sepush.co.za/business/2.0/area?id="+area_id
    response = requests.request("GET", url, data=payload, headers=headers)
    text = response.text
    split = json.loads(text)
    sch = split["schedule"]
    events = split["events"]
    days = sch["days"]
    today = ""
    for i in range(len(days)):
        if days[i]["date"] == date:
            today = days[i]
            break
    stages = today["stages"]
    stages = str(stages)
    stages = stages.split("],")
   
    largest_stage = ""

    times_list = []

    for i in stages:
        i = i.replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        times_list.append(i)

    fin_out = ""

    for i in events:
        event_start = i["start"]
        event_start_time=str(event_start).split("T")[1].split("+")[0][:-3]
        event_end = i["end"]
        event_end_time=str(event_end).split("T")[1].split("+")[0][:-3]
        file = open(file_location+"/log.txt","r+")
        lines = file.readlines()
        if date in event_start or date in event_end:
    
            currently_loadshedding = (event_start_time < current_time and current_time < event_end_time)
            outlier = event_end_time < event_start_time
            stage = int(str(i["note"]).split(" ")[1])
            fin_out = fin_out + "|stage: " + str(stage)
            #print(event_start_time, event_end_time)
            req = 'https://maker.ifttt.com/trigger/receive_loadshedding_time/with/key/'+ifttt_key+'?value1='+event_start_time+'&value2='+event_end_time+'&value3='+str(stage)
            req_w_date = date+" - "+req
            if not currently_loadshedding:
                if not outlier:
                    if req_w_date+"\n" not in lines:
                        requests.post(req)
                        fin_out = fin_out  + " - "+event_start_time+"-"+event_end_time+" => request made| "
                        file.write(req_w_date+'\n')
                    else:
                        fin_out = fin_out + " - "+event_start_time+"-"+event_end_time+" => already there| "
                elif outlier and current_time > event_end_time:
                    if req_w_date+"\n" not in lines:
                        requests.post(req)
                        fin_out = fin_out  + " - "+event_start_time+"-"+event_end_time+" => request made| "
                        file.write(req_w_date+'\n')
                    else:
                        fin_out = fin_out + " - "+event_start_time+"-"+event_end_time+" => already there| "
    if len(fin_out)<=0:
        fin_out = "no loadshedding"
    print(fin_out)
    file.close()
else:
     print(date+" "+ current_time+" - quota exceded")
