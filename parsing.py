#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
#import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from argparse import ArgumentParser  
import telegram
from telegram import InputMediaPhoto

TOKEN = 'token'
chat_id = "chat_id"
keysearch = "key words"

ap = ArgumentParser()
ap.add_argument('-t', '--TOKEN', default=TOKEN, type = str, help='nput token bot, 46 symbols')
ap.add_argument("-i", "--chat_id",default=chat_id, type=str, help="input id chat or user id")
ap.add_argument("-s", "--search",type=str,default=keysearch,help="word for seach")
a = ap.parse_args()
chat_id = a.chat_id
keysearch = a.search

# photos = []
media_group = []

bot = telegram.Bot(token=a.TOKEN)

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
options.add_argument('--incognito')
wd = webdriver.Chrome(options=options)
wd.get(f"https://www.kufar.by/l?query={keysearch}")
wd.implicitly_wait(20)

def get_photo(link):
  photo_link = []
  wd.get(link)
  try:
    soup_photo = bs(wd.page_source, "html.parser")
    soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__lc2v_")
    description = soup_photo.find("h2", class_="styles_description__title__H_4cK").next_sibling.text
    if len(description) > 900:
      description = description[:900]
    for photo in soup_find_all_photo:
      if photo["src"] not in photo_link:
          photo_link.append(photo["src"])
  except:
    pass        
  return photo_link, description
 
soup = bs(wd.page_source, "html.parser")
soupfind = soup.find("a", class_="styles_wrapper__pb4qU")
link = soupfind["href"]
names = soup.find("h3")
price = soup.find("p", class_="styles_price__x_wGw")
img_url = soup.find("img", class_="styles_image--blur__6MsOZ lazyload")["data-src"]
vip = soup.find("a", class_="styles_polepos__nL2AH")

file = f'Объявление: {names.text}, Цена: {price.text}, Ссылка: {link}'
if vip != None:
    vip = vip.find("img")["alt"]
    file = f'{vip} Объявление: {names.text}, Цена: {price.text}, Ссылка: {link}'

for number, url in enumerate(get_photo(link)[0]):
    if number == 0:
      media_group.append(InputMediaPhoto(media=url, caption=file + ", Описание: " + get_photo(link)[1]))
    media_group.append(InputMediaPhoto(media=url))
wd.quit()

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={file}"
#photo = f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}&caption={file}&photo={img_url}'

if t != file:
    bot.send_media_group(chat_id=chat_id, media=media_group)
    #requests.post(url)
    with open('./test.txt', 'w') as f:
      f.write(file)
      f.close()
