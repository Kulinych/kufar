#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
import requests
from argparse import ArgumentParser
import telegram
from telegram import InputMediaPhoto
import sqlite3
import creat_db

TOKEN = "Token"
chat_id = "chat_id"
keysearch = "сноуборд"

con = sqlite3.connect('kufar.db')
curr = con.cursor()
url_photo = 'https://rms.kufar.by/v1/gallery/'

def update(data):
    with con:
        curr.execute(data)


def read(data):
    with con:
        curr.execute(data)
        return curr.fetchone()


def get_photo(link):
    # парсинг фотографий и описания
    photo_link = []
    description = 'Описание не найдено'
    a = requests.get(link)
    try:
        soup_photo = bs(a.content, "html.parser")
        soup_find_all_photo = soup_photo.findAll("img", class_="styles_slide__image__YIPad", limit=9)
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
    photo = []
    try:
        response = requests.get(f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?lang=ru&query={keysearch}').json()
        for ads in response['ads']:
            link = ads['ad_link']
            names = ads['subject']
            ad_id = ads['ad_id']
            if int(ads['price_byn']) != 0:
                price = int(ads['price_byn']) / 100
            else: price = "Договорная"
            for imgs in ads['images']:
                photo.append(url_photo + imgs['path'])
        return link, names, price, ad_id, photo
    except: pass


def main():
    media_group = []
    link, names, price, ad_id, photo = get_api()
    file = f'Объявление: {names}, Цена: {price} '
    if get_photo(link):
        for number, url in enumerate(get_photo(link)[0]):
            if number == 0:
                media_group.append(InputMediaPhoto(media=url, parse_mode='HTML', caption=file + "<a href='" + link + "'>Ссылка</a>, Описание: " + get_photo(link)[1]))
            media_group.append(InputMediaPhoto(media=url))
    if read("SELECT ad_id, price FROM ad WHERE ad_id = %s" % str(ad_id)) is None:
        update('INSERT INTO ad (ad_id, name, price,  date) VALUES ("%s", "%s", "%s", DATETIME("NOW"))' % (ad_id, names, price))
        if len(media_group):
            bot.send_media_group(chat_id=chat_id, media=media_group)
        else: bot.send_message(text=file + link, chat_id=chat_id)
    else:
        r, price_old = read("SELECT ad_id, price FROM ad WHERE ad_id = %s" % str(ad_id))
        if r:
            if r == ad_id:
                print(float(len(str(price_old))))
                if not ((price - 3 < price_old < price + 3) or (price - 500 < price_old < price + 500 and len(str(price_old)) > 5)):
                    update("UPDATE ad SET price = %s WHERE ad_id = %s" % (price, ad_id))
                    if len(media_group):
                        bot.send_media_group(chat_id=chat_id, media=media_group)
                    else: bot.send_message(text=file + link, chat_id=chat_id)


if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument('-t', '--TOKEN', default=TOKEN, type=str, help='input token bot, 46 symbols')
    ap.add_argument("-i", "--chat_id", default=chat_id, type=str, help="input id chat or user id")
    ap.add_argument("-s", "--search", type=str, default=keysearch, help="word for search")
    a = ap.parse_args()

    chat_id = a.chat_id
    keysearch = a.search
    bot = telegram.Bot(token=a.TOKEN)
    main()
