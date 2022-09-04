# parsing 
This script send notice telegram channel when new AD in keysearch on kufar.by 

Change file on executable chmod +x parsing.py

Edit crontab -e

Add crontab job */3 * * * * ~/parsing/parsing.py >/dev/null 2>&1 
