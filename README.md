# Parsing Kufar.by  
This script send notice telegram channel when new AD in keysearch on kufar.by 

Edit TOKEN and Chat_id on you.  

Run console pip install -r requirements.txt

Change file on executable chmod +x parsing.py

Edit crontab -e

Add crontab job */3 * * * * ~/parsing.py >/dev/null 2>&1 
