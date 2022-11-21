# Parsing Kufar.by  
This script send notice telegram channel when new AD in keysearch on kufar.by 

Edit TOKEN and Chat_id on you.  

Add chrome-wedriver:
 Debian/Ubuntu OS
 sudo apt install chromium-driver

 Alpine OS
 sudo apk add chromium-chromedriver

 Other OS
 https://chromedriver.chromium.org/

Run console pip3 install -r requirements.txt
 
Change file on executable chmod +x parsing.py

Edit crontab -e

Add crontab job */3 * * * * ~/parsing.py >/dev/null 2>&1 


*****
DOCKER 

Docker build:

docker build -t parsing:latest .

How to run:

docker run -it -v ~/:/data parsing:latest -t token -i chat_id -s сноуборд