# esp-loadshedding-times

Get the loadshedding times for the day, and send a webhook via Make to update your Google Calendar

# Prerequisites:

- A Make Account - https://www.make.com
- A Google Account
- An EskomSePush API token (Instuctions to get the token are on their website) - https://eskomsepush.gumroad.com/l/api
- A Linux machine to run cronjobs

# STEPS:

- Download the above files to your desired file_location
- Go to https://www.make.com and create a scenario
- Click More -> Import Blueprint and select the blueprint.json file
- Go under the Google Calendar module and sign into your account
- Go under the Webhook module and create a webhook
- Under the webhook advanced settings allow json pass-through
- Fill in the information required in the eskom.py file
- To find your area id run the find_location.py and enter the required info
- create the following cronjobs:
  - SHELL=/bin/sh
  - PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:file_location
  - 45 \* \* \* \* /usr/bin/python3 file_location/eskom.py >> file_location/outputs.txt
  - 57 23 \* \* \* /usr/bin/python3 file_location/copy_to_all_logs.py
  - 58 23 \* \* \* rm file_location/log.txt
  - 59 23 \* \* \* echo "" > file_location/log.txt
