# esp-loadshedding-times
Get the loadshedding times for the day, and send a webhook via IFTTT to update your Google Calendar

# Prerequisites:
  - An IFTTT account
  - A Google Account
  - An EskomSePush API token (Instuctions to get the token are on their website)
  - A Linux machine to run cronjobs

# STEPS:
  - Create an IFTTT Applet to recieve a webhook (be sure to update the eskom.py file with the webhook key)
  - Fill in the information required in the eskom.py file
  - create the following cronjobs:
    - 45 * * * * /usr/bin/python3 file_location/eskom.py >> file_location/outputs.txt
    - 57 23 * * * /usr/bin/python3 file_location/copy_to_all_logs.py
    - 58 23 * * * rm file_location/log.txt
    - 59 23 * * * echo "" > file_location/log.txt
    
