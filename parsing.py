#! /usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import telegram
from telegram import InputMediaPhoto



TOKEN = "token"
chat_id = "chat_id"
keysearch = "сноуборд"
photos = []
bot = telegram.Bot(token=TOKEN)
try:
    f = open('./test.txt', 'r')
except:
    f = open('./test.txt', 'x')
    f.close()
finally:
    f = open('./test.txt', 'r')
    t = f.read()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome(options=options)
wd.get(f"https://www.kufar.by/l?query={keysearch}")
wd.implicitly_wait(20)

soup = bs(wd.page_source, "html.parser")
soupfind = soup.find("a", class_="styles_wrapper__pb4qU")
link = soupfind["href"]
link_photo = wd.get(link)
names = soup.find("h3")
price = soup.find("p", class_="styles_price__x_wGw")

soup_photo = bs(wd.page_source, "html.parser")
soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__lc2v_")
for photo in soup_find_all_photo:
    if photo["src"] not in photos:
        photos.append(photo["src"])
wd.close()

media_group = []

for number, url in enumerate(photos):
    media_group.append(InputMediaPhoto(media=url, caption=names.text + price.text))


file = f'Объявление: {names.text}, Цена: {price.text}, Ссылка: {link}'

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={file}"
# message = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}&caption={file}&photo={photos}'

if t != file:
    bot.send_media_group(chat_id=chat_id, media=media_group)
    requests.post(url)
    with open('./test.txt', 'w') as f:
      f.write(file)

