#!/usr/bin/env python3
import telebot
import time
import sys
from LaTeX2IMG import LaTeX2IMG
from time import sleep
from threading import current_thread
from telebot import logging

TOKEN = ''


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            if text[0:7] == "/latex ":
                text = text[7:]
            elif text[0] == "@":
                text = text[13:]
            else:
                break

            tb.send_chat_action(chatid,'upload_document')

            filename = 'resultado' + current_thread().name

            LaTeX2IMG.main(['LaTeX2IMG',text,filename,'webp'])

            with open(filename + '.webp','rb') as equation:
                tb.send_sticker(chatid, equation)

with open("token.txt","r") as file:
    TOKEN = file.readline().strip()

logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                                  '%m-%d %H:%M:%S')
ch = logging.FileHandler("log.txt")
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)

tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener) #register listener
tb.polling(True)

while True: # Don't let the main Thread end.
    sleep(5)
