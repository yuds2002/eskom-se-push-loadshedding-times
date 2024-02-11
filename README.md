# esp-loadshedding-times
Get the loadshedding times for the day, and send a webhook via IFTTT to update your Google Calendar

# Prerequisites:
  - An IFTTT account
  - A Google Account
  - An EskomSePush API token (Instuctions to get the token are on their website)
  - A Linux machine to run cronjobs

# STEPS:
  - Download the above files to your desired file_location
  - Create an IFTTT Applet to recieve a webhook (be sure to update the eskom.py file with the webhook key)
  - the webhook should recieve two values:
    - value1: the starting time
    - value2: the ending time
  - the Webhook name should be: receive_loadshedding_time
  - Fill in the information required in the eskom.py file
  - To find your area id run the following command with your area inforamtion:
    - curl --location 'https://developer.sepush.co.za/business/2.0/areas_search?text=your_area_name' --header 'token:your-EskomSePush-API-token'
    - the above will return areas with your area name in them, find your specific area and copy the id to the eskom.py file
  - create the following cronjobs:
    - SHELL=/bin/sh
    - PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:file_location
    - 45 * * * * /usr/bin/python3 file_location/eskom.py >> file_location/outputs.txt
    - 57 23 * * * /usr/bin/python3 file_location/copy_to_all_logs.py
    - 58 23 * * * rm file_location/log.txt
    - 59 23 * * * echo "" > file_location/log.txt
