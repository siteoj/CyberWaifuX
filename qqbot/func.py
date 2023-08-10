from pycqBot.cqHttpApi import cqHttpApi, cqLog,cqBot
from pycqBot.data import Message
from waifu.Waifu import Waifu
from waifu.Tools import divede_sentences
import logging
import json
import os
import time
from snownlp import SnowNLP
from pycqBot.cqCode import image, record
from pycqBot.data import Private_Message,Group_Message
from vits.vits import vits
import requests
from vits.fanyi import fanyi
import urllib.request
import json,threading
from newvits.vits import voice_vits
from vits.web import sendprompt,upscale
from controler.control import newthread_process
class message_handler():
    def __init__(self,bot:cqBot,waifu:Waifu) -> None:
        self.last_pic=''
        self.bot=bot
        self.waifu = waifu
        self.sdv = True
        self.fenju = False
        self.ql = False
    # Logs into qzone
    def handle_login_qzone(self,):
        self.waifu.qzonebot.login()

    # Connects to VITS
    # def handle_connect_vits(self,):
    #     self,waifu.v = vits()

    # Sends a voice message 
    def handle_send_voice(message):
        text = fanyi(message.message.replace('#发送语音', ''))
        path = voice_vits(text) 
        message.sender.send_message("%s" % record(file='file:///' + path))
        message.sender.send_message(text)
        
    # Posts to qzone  
    def handle_send_post(self,message):
        if message.sender.id != waifu.qq_number:
            message.sender.send_message('你在想什么呢,让我给你发说说?')
            return
        self.waifu.ss(message)

    # Disables group chat
    def handle_disable_group(self,message:Message):
        self.ql = False
        message.sender.send_message('关闭群聊成功')

    # Enables group chat
    def handle_enable_group(self,message:Message):
        self.ql = True
        message.sender.send_message('打开群聊成功')
    # Turns off voice 
    def handle_turn_off_voice(self,message:Message):
        self.sdv = False
        message.sender.send_message('关闭语音成功')

    # Turns on voice
    def handle_turn_on_voice(self,message:Message):
        self.sdv = True
        message.sender.send_message('打开语音成功') 

    # Turns off sentence splitting
    def handle_turn_off_split(self,message:Message):
        self.fenju = False
        message.sender.send_message('关闭分句成功')

    # Turns on sentence splitting
    def handle_turn_on_split(self,message:Message):
        self.fenju = True
        message.sender.send_message('打开分句成功')
    # Saves memory
    def handle_save_memory(self,):
        self.waifu.summarize_memory()

    def handle_armor_mode(self,message:Message):
        self.waifu.armor_flag = True
        print('开启叠甲成功')
        message.sender.send_message('开启叠甲成功')
        
    def handle_send_text(self,message:Message):
        text = message.message.replace('#话术 ', '')
        self.waifu.brain.think(text)
        print('发送话术成功')
        message.sender.send_message('发送话术成功')

    def handle_init(self,message:Message, bot:cqBot):
        ntp = threading.Thread(target=newthread_process, args=(self.waifu,bot))
        ntp.start()
        print('初始化成功')
        message.sender.send_message('初始化成功')

    def upscaler(self,message:Message):
        print('upscaling')
        target=message.message.replace('#upscale ','')
        url=upscale(self.last_pic,int(target))
        print(url)
        if url != '':
            print('绘图成功')
        else:
            print('failed')
            message.sender.send_message('failed')
            return
        # print(url)

        # urllib.request.urlretrieve(url=url,filename='./mid.png')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        r = requests.get(url=url, headers=headers)

        # print(r.text)

        with open(r'C:\Users\Administrator\Desktop\AnimeWaifu\mid.png','wb') as f:
            f.write(r.content)
        message.sender.send_message('Success')
        message.sender.send_message(image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
        return
    def paint(self,message:Message):
        print('进入绘图')
        prompt = message.message.replace('#绘图 ','')
        self.last_pic,url=sendprompt(prompt)
        print(url)
        if url != '':
            print('绘图成功')
        print(url)

        # urllib.request.urlretrieve(url=url,filename='./mid.png')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        r = requests.get(url=url, headers=headers)

        # print(r.text)

        with open(r'C:\Users\Administrator\Desktop\AnimeWaifu\mid.png','wb') as f:
            f.write(r.content)
        message.sender.send_message(image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
        return
    def changepkg(self,message:Message,v:vits):
        pkg=message.message.replace('#更改包','')
        v.change('model='+pkg)
        print('更改包成功')
        message.sender.send_message('更改包成功')
        return
    def changemodel(self,message:Message,v:vits):
        model=message.message.replace('#更改模型','')
        v.change('speaker='+model)
        print('更改模型成功')
        message.sender.send_message('更改模型成功')
        return
    def send_private_voice(self,message:Message,v:vits):
        print('开始单独发送语音')
        cmd=message.message.replace('#单独发送语音','')
        print(cmd)
        cmds=cmd.split('|')
        aim=int(cmds[0])
        content=cmds[1]
        print(aim)
        print(content)
        ans=fanyi(content)
        print(ans)
        path=v.sendmsg(ans)
        # time.sleep(5)
        path = path.replace("b'",'')
        path = path.replace("'",'')
        print(path)
        self.bot.cqapi.send_private_msg(aim,content)
        self.bot.cqapi.send_private_msg(aim,ans)
        self.bot.cqapi.send_private_msg(aim,"%s" % record(file='file:///' + path))
        logging.info('发送成功！')
        return
    def send_group_voice(self,message:Message,v:vits):
        print('开始发送群聊语音')
        cmd=message.message.replace('#发送群聊语音','')
        print(cmd)
        cmds=cmd.split('|')
        aim=int(cmds[0])
        content=cmds[1]
        print(aim)
        print(content)
        ans=fanyi(content)
        print(ans)
        path=v.sendmsg(ans)
        # time.sleep(5)
        path = path.replace("b'",'')
        path = path.replace("'",'')
        print(path)
        self.bot.cqapi.send_group_msg(aim,content)
        self.bot.cqapi.send_group_msg(aim,ans)
        self.bot.cqapi.send_group_msg(aim,"%s" % record(file='file:///' + path))
        logging.info('发送成功！')
        return