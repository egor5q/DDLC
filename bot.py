# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')
nltk.download('WordNet')
nltk.download('pros_cons')
nltk.download('рейтер')
nltk.download('hmm_treebank_pos_tagger')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('universal_tagset')
nltk.download('averaged_perceptron_tagger_ru')
nltk.download('averaged_perceptron_tagger')
nltk.download('rslp')
nltk.download('porter_test')
nltk.download('vader_lexicon')
nltk.download('treebank')
nltk.download('dependency_treebank')

cutes=['милая','милашка']
monika = telebot.TeleBot(os.environ['monika'])
sayori = telebot.TeleBot(os.environ['sayori'])
yuri = telebot.TeleBot(os.environ['yuri'])
natsuki = telebot.TeleBot(os.environ['natsuki'])

nstats={
    'cute':{},
    'ban':[]
}

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

#---------------------------------Monika handlers start-------------------------------------------------------

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
      t=threading.Timer(4,sendm,args=[m.chat.id,monika,hello,'CAADAgADMQUAAh47XQXbuhY0MkazFwI'])
      t.start()
      if 'миленькой Нацуки' in hello:
         t=threading.Timer(5,sendact,args=[m.chat.id,natsuki,'typing'])
         t.start()
         t=threading.Timer(7,sendm,args=[m.chat.id,natsuki,'Я не миленькая!!!!','CAADAgADJQUAAh47XQVR4niIEFL99wI'])
         t.start()
      
@monika.message_handler(commands=['test'])
def testt(m):
   if m.from_user.id==441399484:
      sendact(m.chat.id, monika, 'typing')
      t=threading.Timer(4,sendm,args=[m.chat.id,monika,'Нацуки, ты такая милая)','CAADAgADMQUAAh47XQXbuhY0MkazFwI'])
      t.start()
      t=threading.Timer(5,sendact,args=[m.chat.id,natsuki,'typing'])
      t.start()
      t=threading.Timer(7,sendm,args=[m.chat.id,natsuki,'Я не милая!!!!','CAADAgADJQUAAh47XQVR4niIEFL99wI'])
      t.start()
      
  
#---------------------------------Monika handlers end-------------------------------------------------------

#---------------------------------Natsuki handlers start-------------------------------------------------------

@natsuki.message_handler()
def natsukki(m):
  if m.from_user.id not in nstats['ban']:
    ps = PorterStemmer()
    text=sent_tokenize(m.text)
    cute=0
    for ids in text:
        i=ids.lower()
        try:
          if 'нацуки' in i or m.reply_to_message.from_user.id==769334999:
            allwords=word_tokenize(i)
            lastword=None
            for idss in allwords:
                word=ps.stem(idss)
                if word in cutes and lastword!='не':
                    cute=1
                lastword=word
        except:
          pass
    if cute==1:
        try:
            if nstats['cute'][m.from_user.id]['cutecount']==1:
                text='Хватит называть меня милой!'
                stick='CAADAgADJAUAAh47XQWqrQRHYiQ3hgI'
                nstats['cute'][m.from_user.id]['cutecount']+=1
            elif nstats['cute'][m.from_user.id]['cutecount']==2:
                del nstats['cute'][m.from_user.id]
                text='Я обиделась.'
                stick='CAADAgADKAUAAh47XQVTttoUBXCT0gI'
                nstats['ban'].append(m.from_user.id)
                t=threading.Timer(300,n_unban,args=[m.from_user.id])
                t.start()
            else:
                pass
        except:
            nstats['cute'].update(createcute(m.from_user.id))
            text='Эй! Я не милая!'
            stick='CAADAgADJQUAAh47XQVR4niIEFL99wI'
        sendm(m.chat.id, natsuki,text,stick)
            
            
def n_unban(id):
    try:
        nstats['ban'].remove(id)
    except:
        pass

def createcute(id):
  return {id:{'id':id,
              'cutecount':1
             }
         }
  
def sendact(id,bot,act):
   bot.send_chat_action(id,act)
      
def sendm(id,bot,text,sticker=None,parse_mode=None):
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

