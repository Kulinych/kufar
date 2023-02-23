# Parsing Kufar.by  
This script send notice telegram channel when new AD in keysearch on kufar.by 

Edit TOKEN and Chat_id on you.  

Run console:
```bash
pip3 install -r requirements.txt
```
 
Change file on executable:
```bash
chmod +x parsing.py
```

Edit crontab:
```bash
crontab -e
```

Add crontab job: 
```bashе 
*/3 * * * * ~/parsing.py >/dev/null 2>&1 
```
or if need more then one:
```bash
*/3 * * * * ~/parsing.py -t [TOKEN] -c [CHAT_ID] -s [KEYSEARCH]>/dev/null 2>&1 
```
*****
DOCKER 

Docker build:

```bash
docker build -t parsing:latest .
```

How to run:
```bash
docker run -it -v ~/:/data parsing:latest -t token -i chat_id -s сноуборд
```
