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

goodmonika=['классная','молодец','супер','красивая','умная','умница']
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
    elif m.reply_to_message!=None:
        if m.from_user.id in mstats['help'] and m.reply_to_message.from_user.id==780744403:
            try:
                answer=0
                ds=['1','2','3','4','5','6','7','8','9','0']
                sm=['+','-',')','(',':','/','>','<','=','*','^']
                i=0
                quest=[]
                for ids in m.text:  # Сразу возводим числа в степени; quest на выходе состоит из str - чисел и знаков
                    quest.append(ids)
                z=0
                for idss in quest:
                    p_otv=''
                    nmb=z
                    cnt=0
                    while quest[nmb] in ds:
                        p_otv+=quest[nmb]
                        nmb+=1
                        cnt+=1
                        if len(quest)==nmb:
                            break
                    while cnt>0:
                        quest.pop(z)
                        cnt-=1
                    if p_otv!='':
                        quest.insert(z,float(p_otv))
                    z+=1
                answ=[]
                i=0
                for ids in quest:
                    if ids=='(':
                        skobka=[]
                        start=i
                        finish=i
                        toremove=[]
                        while quest[finish]!=')':
                            if quest[finish]!='(' and quest[finish]!=')':
                                skobka.append(quest[finish])
                            toremove.append(finish)
                            finish+=1
                        z=0
                        for idss in skobka:
                            p_otv=''
                            nmb=z
                            cnt=0
                            while skobka[nmb] in ds:
                                p_otv+=skobka[nmb]
                                nmb+=1
                                cnt+=1
                                if len(skobka)==nmb:
                                    break
                            while cnt>0:
                                skobka.pop(z)
                                cnt-=1
                            if p_otv!='':
                                skobka.insert(z,float(p_otv))
                            z+=1
                        toremove.append(finish)
                        otv=calculate(skobka)
                        r=toremove[0]
                        for idss in toremove:
                            quest.pop(r)
                        quest.insert(start,otv)
                    else:
                        pass
                    i+=1
                z=0
                for idss in quest:
                        p_otv=''
                        nmb=z
                        cnt=0
                        while quest[nmb] in ds:
                            p_otv+=quest[nmb]
                            nmb+=1
                            cnt+=1
                            if len(quest)==nmb:
                                break
                        while cnt>0:
                            quest.pop(z)
                            cnt-=1
                        if p_otv!='':
                            quest.insert(z,float(p_otv))
                        z+=1
                i=0
                print(quest)
                for ids in quest:
                    try:
                        a=int(ids)
                        quest.pop(i)
                        quest.insert(i,a)
                    except:
                        pass
                    i+=1
                otvet=calculate(quest)
                try:
                    mstats['help'].remove(m.from_user.id)
                except:
                    pass
                t=threading.Timer(1,giveansw,args=[m.chat.id,otvet])
                t.start()
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                monika.send_message(441399484, traceback.format_exc())
            ps = PorterStemmer()
        text=sent_tokenize(m.text)
        cute=0
        for ids in text:
            i=ids.lower()
            try:
              if 'моника' in i or m.reply_to_message.from_user.id==780744403:
                allwords=word_tokenize(i)
                lastword=None
                for idss in allwords:
                    word=ps.stem(idss)
                    if word in goodmonika and lastword!='не':
                        cute=1
                    lastword=word
            except:
              pass
        if cute==1:
            gds=['Ой, спасибо)','Да ладно тебе)','Ты меня смущаешь...)']
            t=threading.Timer(1,sendact,args=[m.chat.id,monika,'typing'])
            t.start()
            t=threading.Timer(3.5,sendm,args=[m.chat.id,monika,random.choice(gds)])
            t.start()
                   
def giveansw(id,otvet):
    monika.send_chat_action(id,'typing')
    t=threading.Timer(1.5,sendm,args=[id,monika,'Хмм... Подожди пару секунд.'])
    t.start()
    t=threading.Timer(4,sendact,args=[id,monika,'typing'])
    t.start()
    t=threading.Timer(6,sendm,args=[id,monika,'Судя по моим расчётам, будет `'+str(otvet)+'`. Не благодари!','CAADAgADMwUAAh47XQVxmIa4ZBC_UQI','markdown'])
    t.start()
                     


def calculate(msv):
    otv=0
    i=0
    while i<len(msv):
        if msv[i]=='^':
            prm=msv[i-1]
            o=1
            while o<msv[i+1]:
                prm=prm*msv[i-1]
                o+=1
            msv.pop(i-1)
            msv.pop(i-1)
            msv.pop(i-1)
            otv+=prm
            msv.insert(i-1,prm)
            i-=1
        i+=1
    i=0
    while i<len(msv):
        if msv[i]=='*':
            prm=msv[i-1]*msv[i+1]
            msv.pop(i-1)
            msv.pop(i-1)
            msv.pop(i-1)
            otv+=prm
            msv.insert(i-1,prm)
            i-=1
        elif msv[i]=='/' or msv[i]==':':
            prm=msv[i-1]/msv[i+1]
            msv.pop(i-1)
            msv.pop(i-1)
            msv.pop(i-1)
            otv+=prm
            msv.insert(i-1,prm)
            i-=1
        i+=1
    i=0
    while i<len(msv):
        if msv[i]=='+':
            prm=msv[i-1]+msv[i+1]
            msv.pop(i-1)
            msv.pop(i-1)
            msv.pop(i-1)
            otv+=prm
            msv.insert(i-1,prm)
            i-=1
        elif msv[i]=='-':
            prm=msv[i-1]-msv[i+1]
            msv.pop(i-1)
            msv.pop(i-1)
            msv.pop(i-1)
            otv+=prm
            msv.insert(i-1,prm)
            i-=1
        i+=1
    print(msv)
    otv=0
    for ids in msv:
        try:
            otv+=ids
        except:
            pass
    return otv
                       
            

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
        sendact(m.chat.id,natsuki,'typing')
        t=threading.Timer(2,sendm,args=[m.chat.id, natsuki,text,stick])
        t.start()
      
    
#---------------------------------Natsuki handlers end-------------------------------------------------------

#---------------------------------Sayori handlers start-------------------------------------------------------

def s_where():
    x=['нацуки','моника','сайори','юри','кексы','кексики','печенье']

def sayoritext(name):
    x=['Привет, '+name+'! Прости, но я пока что не могу с тобой поговорить, давай попозже.']
    return random.choice(x)
    
@sayori.message_handler()
def sayoritalks(m):
    ps = PorterStemmer()
    text=sent_tokenize(m.text)
    s=0
    answer=0
    for ids in text:
        i=ids.lower()
        if 'сайори' in i or 'саёри' in i or m.reply_to_message.from_user.id==769334999:
            answer=1
            allwords=word_tokenize(i)
            lastword=None
            c=0
            for idss in allwords:
                word=ps.stem(idss)
                if word=='где':
                    for idsss in allwords:
                        if idsss in s_where():
                            pass
                lastword=word
                c+=1
    if answer==1:
        text=sayoritext(m.from_user.first_name)
        sendact(m.chat.id,sayori,'typing')
        t=threading.Timer(3,sendm,args=[m.chat.id, sayori,text,'CAADAgAD8wEAAp5JcwLpSZKYdw46_AI'])
        t.start()
    
    
def mremove(id,chatid):
    try:
        mstats['help'].remove(id)
        monika.send_chat_action(chatid,'typing')
        t=threading.Timer(3,sendm,args=[chatid,monika,'Ты, наверное, уже не помнишь свой вопрос. Ничего страшного, такое бывает. Подходи, как вспомнишь!','CAADAgADMwUAAh47XQVxmIa4ZBC_UQI'])
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

