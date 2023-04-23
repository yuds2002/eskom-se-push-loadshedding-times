from datetime import datetime
import requests
import json
payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}
date= datetime.today().strftime('%Y-%m-%d')
#print(date)

url = "https://developer.sepush.co.za/business/2.0/api_allowance"
response = requests.request("GET", url, headers=headers, data=payload)
text = json.loads(response.text)
count = int(text["allowance"]["count"])

current_time = datetime.today().strftime('%H:%M')


if count < 50:
    url = "https://developer.sepush.co.za/business/2.0/area?id=capetown-5-claremont"
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

    #print(times_list)
    
    fin_out = ""

    for i in events:
        event_start = i["start"]
        event_start_time=str(event_start).split("T")[1].split("+")[0][:-3]
        event_end = i["end"]
        event_end_time=str(event_end).split("T")[1].split("+")[0][:-3]
        file = open("log.txt","r+")
        lines = file.readlines()
        if date in event_start or date in event_end:
            #print(i)
            
            stage = int(str(i["note"]).split(" ")[1])
            fin_out = fin_out + "|stage: " + str(stage)
            #print(event_start_time, event_end_time)

            req = 'https://maker.ifttt.com/trigger/recieve_loadshedding_time/with/key/FctvAiSHAmO0BMOKF4YhO?value1='+event_start_time+'&value2='+event_end_time+'&value3='+str(stage)
            req_w_date = date+" - "+req
            if req_w_date+"\n" not in lines:
                file.write(req_w_date+'\n')
                fin_out = fin_out  + " - "+event_start_time+"-"+event_end_time+" => request made| "
                requests.post(req)
            else:
                fin_out = fin_out + " - "+event_start_time+"-"+event_end_time+" => already there| "

            #times = str(times_list[stage-1]).split(",")
            #
            #for t in times:
            #    time = t.split("-")
            #    if time[0] >= event_start_time and time[1]>=event_end_time:
            #        print("stage",stage, time)
    print(fin_out)
    file.close()
else:
     print(date+" "+ current_time+" - quota exceded")
