#! /usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

TOKEN = "Tokenbot"
chat_id = "ID chat for send message"
keysearch ="one key"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome(options=options)
wd.get(f"https://www.kufar.by/l?ot=1&query={keysearch}&rgn=all&utm_search=Query%20only")
wd.implicitly_wait(20)

soup = bs(wd.page_source, "html.parser")
soupfind = soup.find("a", class_="styles_wrapper__pb4qU")
link = soupfind["href"]
names = soup.find('div', class_="styles_left___v6uP")
file = names.text + link
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={file}"
f = open('./test.txt', 'r')
t = f.read()
if t != file:
    requests.post(url)
    with open('./test.txt', 'w') as f:
      f.write(file)
      f.close()
 
