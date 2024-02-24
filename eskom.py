from datetime import datetime, timedelta
import requests
import json

############
# Input
area_id = "" # eskom area id, please see docs NOTE the string must be lowercase
file_location = "" # folder location of log file
esp_token = "" # EskomSePush API Token
req = "" # Make webhook address
############

payload = {}
headers = {"token" : esp_token}
date= datetime.today().strftime('%Y-%m-%d')
tomorrow = (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')

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
    if "schedule" in split and "events" in split:
        sch = split["schedule"]
        events = split["events"]
        days = sch["days"]
        today = ""
        for i in range(len(days)):
            if days[i]["date"] == date:
                today = days[i]
                break
        fin_out = ""

        for i in events:
            event_start = i["start"]
            event_start_time=str(event_start).split("T")[1].split("+")[0][:-3]
            event_end = i["end"]
            event_end_time=str(event_end).split("T")[1].split("+")[0][:-3]
            event_end_time_hour = event_end_time.split(":")[0]
            if event_end_time_hour > "12":
                event_end_time = str(int(event_end_time_hour)-12)+":"+event_end_time[3::]+" PM"

            file = open(file_location+"/log.txt","r+")
            lines = file.readlines()
            if date in event_start or date in event_end:
        
                currently_loadshedding = (event_start_time < current_time and current_time < event_end_time)
                outlier = event_end_time < event_start_time
                stage = int(str(i["note"]).split(" ")[1])
                fin_out = fin_out + "|stage: " + str(stage)

                event_end_time_wo_date = event_end_time
                event_start_time = date +" "+ event_start_time
                if event_end_time_hour == "00":
                    event_end_time = tomorrow +" "+ event_end_time
                else:
                    event_end_time = date +" "+ event_end_time

                
                var = {'start_time': event_start_time, 'end_time':event_end_time, 'end_time_no_date': event_end_time_wo_date}


                log = "|"+var["start_time"]+"  -  "+var["end_time"]+"|"
                if not currently_loadshedding:
                    if not outlier:
                        if log+"\n" not in lines:
                            requests.post(req, data=var)
                            fin_out = fin_out  + " - "+event_start_time+"-"+event_end_time+" => request made|\n"
                            file.write(log+'\n')
                        else:
                            fin_out = fin_out + " - "+event_start_time+"-"+event_end_time+" => already there|\n"
                    elif outlier and current_time > event_end_time_wo_date:
                        if log+"\n" not in lines:
                            requests.post(req, data=var)
                            fin_out = fin_out  + " - "+event_start_time+"-"+event_end_time+" => request made|\n"
                            file.write(log+'\n')
                        else:
                            fin_out = fin_out + " - "+event_start_time+"-"+event_end_time+" => already there|\n"
        
        if len(fin_out)<=0:
            fin_out = "no loadshedding"
        print(fin_out)
        file.close()
    else:
        print("no loadshedding")
else:
    print(date+" "+ current_time+" - quota exceded")