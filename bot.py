# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient

monika = telebot.TeleBot(os.environ['monika'])
sayori = telebot.TeleBot(os.environ['sayori'])
yuri = telebot.TeleBot(os.environ['yuri'])
natsuki = telebot.TeleBot(os.environ['natsuki'])


client=MongoClient(os.environ['database'])
db=client.ddlc
users=db.users

monika_hello_basic=['Добро пожаловать в литературный клуб! Я всегда мечтала создать уютное место, где можно хорошо провести время. '+\
              'Здесь мы можем совместно улучшать свои навыки в чтении литературы и не только.','Привет, это литературный клуб. '+\
              'Рада тебя видеть здесь, нам сейчас очень нужны новые члены, и ты очень кстати.','Привет! Хорошо, что ты заглянул '+\
                    '- тут мы улучшаем свои навыки в прочтении литературы, и просто проводим время вместе! Надеюсь, что ты останешься '+\
                    'с нами надолго.','Здравствуй, наш дорогой гость! Тут ты сможешь пообщаться с уже вступившими членами клуба - Всегда '+\
                    'весёлой Сайори, начитанной Юри и миленькой Нацуки.','Приветствую тебя в Литературном клубе. Проходи не стесняйся,'+\
                    'Нацуки уже испекла кексики к твоему приходу, а Юри сделает чай, если ты хочешь.']

@monika.message_handler(content_types=['sticker'])
def stickercatch(m):
    monika.send_message(441399484,str(m.sticker.file_id))
    print(m.sticker.file_id)                   
                    
@monika.message_handler(content_types=['new_chat_members'])
def newchatmember(m):
   if users.find_one({'id':m.from_user.id})==None:
      user=m.from_user
      users.insert_one(createuser(user.id,user.first_name))
      hello=random.choice(monika_hello_basic)
      sendact(m.chat.id, monika, 'typing')
      t=threading.Timer(4,sendm,args=[m.chat.id,monika,hello,None,''])
      t.start()
      if 'миленькой Нацуки' in hello:
         t=threading.Timer(5,sendact,args=[m.chat.id,natsuki,'typing'])
         t.start()
         t=threading.Timer(7,sendm,args=[m.chat.id,natsuki,'Я не миленькая!!!!',None,''])
         t.start()
      

def sendact(id,bot,act):
   bot.send_chat_action(id,act)
      
def sendm(id,bot,text,parse_mode=None, sticker=None):
   bot.send_message(id,text,parse_mode=parse_mode)
   if sticker!=None:
       bot.send_sticker(id,sticker)
 

def createuser(id,name):
    return {
        'name':name,
        'id':id
    }

def botpolling(bot):
  bot.polling(none_stop=True,timeout=600)
  
if True:
   print('7777')
   t=threading.Timer(1,botpolling,args=[monika])
   t.start()
   t=threading.Timer(1,botpolling,args=[natsuki])
   t.start()
   t=threading.Timer(1,botpolling,args=[sayori])
   t.start()
   t=threading.Timer(1,botpolling,args=[yuri])
   t.start()

