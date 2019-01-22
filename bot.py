# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
import traceback
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

cutes=['милая','милашка','миленькой','милой','милую']
monika = telebot.TeleBot(os.environ['monika'])
sayori = telebot.TeleBot(os.environ['sayori'])
yuri = telebot.TeleBot(os.environ['yuri'])
natsuki = telebot.TeleBot(os.environ['natsuki'])

def skl(x):
    if x=='Моника':
        return {
            'у':'Моники',
            'с':'Моникой',
            'для':'Моники',
            'перед':'Моникой',
            'после':'Моники'
        }
    elif x=='Нацуки':
        return {
            'у':'Нацуки',
            'с':'Нацуки',
            'для':'Нацуки',
            'перед':'Нацуки',
            'после':'Нацуки'
        }
    elif x=='Юри':
        return {
            'у':'Юри',
            'с':'Юри',
            'для':'Юри',
            'перед':'Юри',
            'после':'Юри'
        }
    elif x=='Сайори':
        return {
            'у':'Сайори',
            'с':'Сайори',
            'для':'Сайори',
            'перед':'Сайори',
            'после':'Сайори'
        }
            

nstats={
    'cute':{},
    'ban':[]
}

mstats={
    'help':[]
}

client=MongoClient(os.environ['database'])
db=client.ddlc
users=db.users

def monikahello(name):
    x=name
    monika_hello_basic=['Добро пожаловать в литературный клуб, '+x+'! Я всегда мечтала создать уютное место, где можно хорошо провести время. '+\
              'Здесь мы можем совместно улучшать свои навыки в чтении литературы и не только.','Привет, это литературный клуб. '+\
              'Рада тебя видеть здесь, нам сейчас очень нужны новые члены, и ты очень кстати.','Привет, '+x+'! Хорошо, что ты заглянул '+\
                    '- тут мы улучшаем свои навыки в прочтении литературы, и просто проводим время вместе! Надеюсь, что ты останешься '+\
                    'с нами надолго.','Здравствуй, наш дорогой гость! Тут ты сможешь пообщаться с уже вступившими членами клуба - Всегда '+\
                    'весёлой Сайори, начитанной Юри и миленькой Нацуки.','Приветствую тебя в Литературном клубе, '+x+'! Проходи не стесняйся,'+\
                    'Нацуки уже испекла кексики к твоему приходу, а Юри сделает чай, если ты хочешь.','Хорошо что ты заглянул, '+x+'! '+\
                        'мы тебя ждали, не стесняйся. Нацуки испекла кексы. А Юри уже готова заварить чай, он у неё получается просто замечательный!',
                       'Ох, ты как раз вовремя, '+x+'! Нацуки только что закончила печь свои кексы, сейчас мы сдвинем пары, и сможем все вместе поесть их!']
    text=random.choice(monika_hello_basic)
    return text
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
      hello=monikahello(m.from_user.first_name)
      sendact(m.chat.id, monika, 'typing')
      t=threading.Timer(4,sendm,args=[m.chat.id,monika,hello,'CAADAgADMQUAAh47XQXbuhY0MkazFwI'])
      t.start()
      if 'миленькой Нацуки' in hello:
          t=threading.Timer(5,sendact,args=[m.chat.id,natsuki,'typing'])
          t.start()
          t=threading.Timer(7,sendm,args=[m.chat.id,natsuki,'Я не миленькая!','CAADAgADJQUAAh47XQVR4niIEFL99wI'])
          t.start()
             
      
@monika.message_handler(commands=['test'])
def testt(m):
   if m.from_user.id==441399484:
      sendact(m.chat.id, monika, 'typing')
      t=threading.Timer(4,sendm,args=[m.chat.id,monika,'Нацуки, ты такая милая)','CAADAgADMQUAAh47XQXbuhY0MkazFwI'])
      t.start()
      t=threading.Timer(5,sendact,args=[m.chat.id,natsuki,'typing'])
      t.start()
      t=threading.Timer(7,sendm,args=[m.chat.id,natsuki,'Я не милая!','CAADAgADJQUAAh47XQVR4niIEFL99wI'])
      t.start()
      
@monika.message_handler()
def monikamessages(m):
    helpp=['помоги','помощь']
    ps = PorterStemmer()
    text=sent_tokenize(m.text)
    hlp=0
    for ids in text:
        i=ids.lower()
        if 'моника' in i:
            allwords=word_tokenize(i)
            for idss in allwords:
                if idss in helpp:
                    hlp=1
    if hlp==1:
        if m.from_user.id not in mstats['help']:
            sendact(m.chat.id, monika, 'typing')
            t=threading.Timer(2,sendm,args=[m.chat.id,monika,'Привет, '+m.from_user.first_name+'. Чем могу помочь?','CAADAgADMQUAAh47XQXbuhY0MkazFwI'])
            t.start()
            mstats['help'].append(m.from_user.id)
            t=threading.Timer(120,mremove,args=[m.from_user.id,m.chat.id])
            t.start()
    if m.from_user.id in mstats['help'] and m.reply_to_message.from_user.id==780744403:
        try:
            answer=0
            ds=['1','2','3','4','5','6','7','8','9','0']
            sm=['+','-',')','(',':','/','>','<','=','*','^']
            i=0
            quest=[]
            for ids in m.text:                    # Сразу возводим числа в степени; quest на выходе состоит из int - чисел и знаков
                if ids=='^':
                    digit=int(m.text[i-1])
                    st=int(m.text[i+1])
                    c=1
                    answ=digit
                    while c<int(st):
                        answ=answ*digit
                        c+=1
                    quest.append(answ)
                else:
                    try:
                        quest.append(int(ids))
                    except:
                        quest.append(ids)
                i+=1
            answ=[]
            i=0
            for ids in quest:
                if ids=='(':
                    skobka=[]
                    start=i
                    finish=start
                    toremove=[]
                    while quest[finish]!=')':
                        skobka.append(quest[finish])
                        toremove.append(finish)
                        finish+=1
                    otv=calculate(skobka)
                    r=toremove[0]
                    for idss in toremove:
                        quest.pop([r])
                    print(quest)
                      
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
            monika.send_message(441399484, traceback.format_exc())
                        
                   
                    
def calculate(msv):
    otv=[]
    for ids in msv:
        if ids=='*':
            pass
                       
            

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
      
    
#---------------------------------Natsuki handlers end-------------------------------------------------------
    
def mremove(id,chatid):
    try:
        mstats['help'].remove(id)
        monika.send_chat_action(chatid,'typing')
        t=threading.Timer(3,sendm,args=[id,monika,'Ты, наверное, уже не помнишь свой вопрос. Ничего страшного, такое бывает. Подходи, как вспомнишь!','CAADAgADMwUAAh47XQVxmIa4ZBC_UQI'])
        t.start()
    except:
        pass

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

