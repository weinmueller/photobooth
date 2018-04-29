# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 18:23:46 2018

@author: Pascha
"""

import time, datetime
import telepot
from telepot.loop import MessageLoop

now = datetime.datetime.now()

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print("Received: %s" % command)

    if command == '/hi':
        telegram_bot.sendMessage (chat_id, str("Hi! CircuitDigest"))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == '/logo':
        telegram_bot.sendPhoto (chat_id, photo = "https://i.pinimg.com/avatars/circuitdigest_1464122100_280.jpg")

def BotMessage(msg):
    telegram_bot.sendMessage(369096940,msg)
        
def BotPhoto(path):
    telegram_bot.sendPhoto (369096940,photo = open(path,'rb'))

telegram_bot = telepot.Bot('575762574:AAGkc7sIIvGopdGfpAdeNP5QdeJzP7JnRcw')
print(telegram_bot.getMe())