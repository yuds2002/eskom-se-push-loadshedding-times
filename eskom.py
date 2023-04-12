from datetime import datetime
import requests
payload = {}
headers = {"token" : "063120A8-A6F64402-9C6D6378-69CDFA5B"}

url = "https://developer.sepush.co.za/business/2.0/api_allowance"
response = requests.request("GET", url, headers=headers, data=payload)
text = response.text

out = text[text.find("count"):text.find('"t')]
out = out.replace('"','').replace(",",' ')
count = out[out.find(":")+1:out.find(" ")]
#print(count)
current_time = datetime.today().strftime('%H:%M')
date= datetime.today().strftime('%Y-%m-%d')
if int(count) < 50:
    url = "https://developer.sepush.co.za/business/2.0/area?id=capetown-5-claremont"
    response = requests.request("GET", url, data=payload, headers=headers)

    text = response.text
    #print(text)
    start = text[text.find('"date":'+'"'+date+'"')::]
    split = start[:start.find("{")].split(",[")

    stage0 = split[0].split("[[")[1] 
    split[0] = stage0 

    offset = len('note":"Stage ')
    stage_begin = text.find('note":"Stage ')+offset
    stage = text[stage_begin:stage_begin+1:]



    times = []
    if int(stage) == 2:
        times = split[int(stage)-1]
    elif (int(stage)+1)<=(len(split)):
        times = split[int(stage)-2]
    else:
        times = split[0]

    times = times.split('",')

    file = open("log.txt","r+")
    lines = file.readlines()

    fin_out = "Stage: "+stage

    if len(times) >= 1:
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
                    fin_out = fin_out  + " - "+i+" => request made"
                    print(fin_out)
                    requests.post(req)
                else:
                    fin_out = fin_out + " - "+i+" => already there"
                    print(fin_out)
            print(fin_out+" - "+ i +" - no more loadshedding today: "+date)
    else:
        fin_out = fin_out+" - no loadshedding => "+date
        print(fin_out)
    file.close()
    

else:
    print(date+" "+current_time+" - quota exceded")




