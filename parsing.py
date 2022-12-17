#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from argparse import ArgumentParser  
import telegram
from telegram import InputMediaPhoto

TOKEN = 'token'
chat_id = "chat_id"
keysearch = "сноуборд"

def get_photo(link):
  # парсинг фотографий и описания
  photo_link = []
  description = 'Описание не найдено'
  wd.get(link)
  try:
    soup_photo = bs(wd.page_source, "html.parser")
    soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__lc2v_", limit=9) 
    for photo in soup_find_all_photo:
      if photo["src"] not in photo_link:
        photo_link.append(photo["src"])
    description = soup_photo.find("h2", class_="styles_description__title__H_4cK").next_sibling.text
    if len(description) > 870:
      description = description[:867] + "..." 
  except: pass
  return photo_link, description       

def get_api():
  # Запрос к APi и парсинг параметров
  try:
    response = requests.get(f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?lang=ru&query={keysearch}').json()
    for ads in response['ads']:
      link = ads['ad_link']
      names = ads['subject']
      if int(ads['price_byn']) != 0:
        price = int(ads['price_byn']) / 100
      else: price = "Договорная"
  except: pass
  return link, names, price

def main():
  media_group = []
  # Проверка наличия файла. 
  try: f = open(keysearch + ".txt", 'r')
  except:
    f = open(keysearch + ".txt", 'x')
    f.close()
  finally:
    f = open(keysearch + ".txt", 'r')
    t = f.read()
  
  link = get_api()[0]
  file = f'Объявление: {get_api()[1]}, Цена: {get_api()[2]}'

  if get_photo(link) != None: 
    for number, url in enumerate(get_photo(link)[0]):
      if number == 0:
        media_group.append(InputMediaPhoto(media=url, parse_mode='HTML', caption=file + "<a href='" + link + "'>Ссылка</a>, Описание: " + get_photo(link)[1]))
      media_group.append(InputMediaPhoto(media=url))
  wd.quit()

  # Запись в файл для сравнения. отправка сообщения 
  if t != file:
      with open(keysearch + ".txt", 'w') as f:
        f.write(file)
        f.close()
      if len(media_group) != 0:
        bot.send_media_group(chat_id=chat_id, media=media_group)  
      else: bot.send_message(text=file + link, chat_id=chat_id)

if __name__ == "__main__":
  ap = ArgumentParser()
  ap.add_argument('-t', '--TOKEN', default=TOKEN, type = str, help='nput token bot, 46 symbols')
  ap.add_argument("-i", "--chat_id",default=chat_id, type=str, help="input id chat or user id")
  ap.add_argument("-s", "--search",type=str,default=keysearch,help="word for search")
  a = ap.parse_args()

  chat_id = a.chat_id
  keysearch = a.search
  
  # Загрузка webdriver с Chrome и дополнительными опциями
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--incognito')
  wd = webdriver.Chrome(options=options)

  bot = telegram.Bot(token=a.TOKEN)
  main()
