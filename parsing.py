#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
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
  a = requests.get(link)
  try:
    soup_photo = bs(a.content, "html.parser")
    soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__FY9R4", limit=9)
    for photo in soup_find_all_photo:
      if photo["src"] not in photo_link:
        photo_link.append(photo["src"])      
    description = soup_photo.find("div", itemprop="description").text
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
    return link, names, price
  except: pass
  

def main():
  media_group = []
  # Проверка наличия файла (костыль). 
  try: f = open(keysearch + ".txt", 'r')
  except:
    f = open(keysearch + ".txt", 'x')
    f.close()
  finally:
    f = open(keysearch + ".txt", 'r')
    t = f.read()
  
  try:
    link, names, price = get_api()
    file = f'Объявление: {names}, Цена: {price} '
  #a = requests.get(link)
  #print(a.content)
    if get_photo(link) != None: 
      for number, url in enumerate(get_photo(link)[0]):
        if number == 0:
          media_group.append(InputMediaPhoto(media=url, parse_mode='HTML', caption=file + "<a href='" + link + "'>Ссылка</a>, Описание: " + get_photo(link)[1]))
        media_group.append(InputMediaPhoto(media=url))
  
  
  # Запись в файл для сравнения. отправка сообщения 
    if t != file:
        with open(keysearch + ".txt", 'w') as f:
          f.write(file)
          f.close()
        if len(media_group) != 0:
          bot.send_media_group(chat_id=chat_id, media=media_group)  
        else: bot.send_message(text=file + link, chat_id=chat_id)
  except: print('Объявлений не найдено')
    
if __name__ == "__main__":
  ap = ArgumentParser()
  ap.add_argument('-t', '--TOKEN', default=TOKEN, type = str, help='nput token bot, 46 symbols')
  ap.add_argument("-i", "--chat_id",default=chat_id, type=str, help="input id chat or user id")
  ap.add_argument("-s", "--search",type=str,default=keysearch,help="word for search")
  a = ap.parse_args()

  chat_id = a.chat_id
  keysearch = a.search
    
  bot = telegram.Bot(token=a.TOKEN)
  main()
