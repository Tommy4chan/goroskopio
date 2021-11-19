import telebot
import schedule
from threading import Thread
from time import sleep
import re
import requests
import bs4
import logging
import os
from telebot.types import Message
from telegram.ext import Updater

token='2131814227:AAHk-hN8ZXOcjXl-28zZynNwczvpHq76wDQ'
NAME = 'goroskopio'
bot = telebot.TeleBot(token)


def schedule_checker():
  while True:
      schedule.run_pending()
      sleep(1)


def function_to_run():
  messageNumber = 0
  messageNumber = int(read_file('data.txt'))
  for x in range(20):
    datareturn = request(messageNumber)
    if datareturn == -1:
      break
    else:
      messageNumber += 1
  write_file('data.txt', messageNumber)  

def request(urli):
  
  url = requests.get('https://t.me/skopogori/' + str(urli) + '?embed=1') #подставляем url

  b = bs4.BeautifulSoup(url.text, "html.parser")
  url1 = b.select('.tgme_widget_message_bubble')
  if re.sub(r"[\n\t\s]*", "", url1[0].getText())[:10].strip() == 'Скопогорыt':
    print("sdfgs")
  elif re.sub(r"[\n\t\s]*", "", url1[0].getText()) == 'Postnotfound':
    print(re.sub(r"[\n\t\s]*", "", url1[0].getText()))
    return -1
  else:
    v = bs4.BeautifulSoup(url.text, "html.parser")
    url2 = v.select('.tgme_widget_message_text')
    url_print = url2[0].getText()
    url_print = url_print
    print(url_print)
    return bot.send_message('-688661978', url_print)
  

  #-688661978
  #-1001493083288

def write_file(filename, intval):
    with open(filename, 'w') as fp:
        print(f'intval: {intval}')
        fp.write(str(intval))


def read_file(filename):
    with open(filename) as fp:
        return fp.read()

if __name__ == "__main__":
    schedule.every().day.at("08:40").do(function_to_run)
    Thread(target=schedule_checker).start() 
    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(token)
    dp = updater.dispatcher
    # Add handlers

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token,
                          webhook_url=f"https://{NAME}.herokuapp.com/{token}")
    updater.idle()

