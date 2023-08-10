from pycqBot.cqHttpApi import cqHttpApi, cqLog
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
fenju=False
ql = False
sdv = True
last_pic=''
def load_config():
    with open(f'./qqbot/bot.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['user_id_list']


def make_qq_bot(callback, waifu: Waifu, send_text, send_voice, tts):
    global sdv
    sdv= send_voice
    cqLog(level=logging.INFO, logPath='./qqbot/cqLogs')

    cqapi = cqHttpApi(download_path='./qqbot/download')
    # def translate(text)
    def process(message :Message,group = False):
        global sdv
        global fenju
        global last_pic
        global ql
        if group and message.sender.id != 169829974:
            return
        if '#叠甲' in message.message:
            waifu.armor_flag = True
            print('开启叠甲成功')
            message.sender.send_message('开启叠甲成功')
            return
        if '#话术' in message.message:
            text=message.message.replace('#话术 ','')
            waifu.brain.think(text)
            print('发送话术成功')
            message.sender.send_message('发送话术成功')
            return
        if '#初始化' in message.message:
            ntp=threading.Thread(target=newthread_process,args=(waifu,bot))
            ntp.start()
            print('初始化成功')
            message.sender.send_message('初始化成功')
            return
        if '#upscale' in message.message:
            print('upscaling')
            target=message.message.replace('#upscale ','')
            url=upscale(last_pic,int(target))
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
        if '#发送群聊画图' in message.message:
            print('发送群聊画图')
            cmd=message.message.replace('#单独发送语音','')
            print(cmd)
            cmds=cmd.split('|')
            prompt=cmd[1]
            aim=cmd[0]
            print('进入绘图')
            last_pic,url=sendprompt(prompt)
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
            bot.cqapi.send_group_msg(int(aim),image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
            return
        if '#绘图' in message.message:
            print('进入绘图')
            prompt = message.message.replace('#绘图 ','')
            last_pic,url=sendprompt(prompt)
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
        if '#保存记忆' in message.message:
            waifu.summarize_memory()
            return
        if '#更改包' in message.message:
            pkg=message.message.replace('#更改包','')
            waifu.v.change('model='+pkg)
            print('更改包成功')
            message.sender.send_message('更改包成功')
            return
        if '#更改模型' in message.message:
            model=message.message.replace('#更改模型','')
            waifu.v.change('speaker='+model)
            print('更改模型成功')
            message.sender.send_message('更改模型成功')
            return
        if '#关闭语音' in message.message:
            sdv=False
            message.sender.send_message('关闭语音成功')
            return
        if '#打开语音' in message.message:
            sdv=True
            message.sender.send_message('打开语音成功')
            return
        if '#关闭分句' in message.message:
            fenju=False
            message.sender.send_message('关闭分句成功')
            return
        if '#打开分句' in message.message:
            fenju = True
            message.sender.send_message('打开分句成功')
            return
        if '#单独发送语音' in message.message:
            print('开始单独发送语音')
            cmd=message.message.replace('#单独发送语音','')
            print(cmd)
            cmds=cmd.split('|')
            aim=int(cmds[0])
            content=cmds[1]
            print(aim)
            print(content)
            ans=waifu.fanyi(content)
            print(ans)
            path=voice_vits(text=ans)
            # time.sleep(5)
            path = path.replace("b'",'')
            path = path.replace("'",'')
            print(path)
            bot.cqapi.send_private_msg(aim,content)
            bot.cqapi.send_private_msg(aim,ans)
            bot.cqapi.send_private_msg(aim,"%s" % record(file='file:///' + path))
            logging.info('发送成功！')
            return
        if '#发送群聊语音' in message.message:
            print('开始发送群聊语音')
            cmd=message.message.replace('#发送群聊语音','')
            print(cmd)
            cmds=cmd.split('|')
            aim=int(cmds[0])
            content=cmds[1]
            print(aim)
            print(content)
            ans=waifu.fanyi(content)
            print(ans)
            path=voice_vits(text=ans)
            # time.sleep(5)
            path = path.replace("b'",'')
            path = path.replace("'",'')
            print(path)
            bot.cqapi.send_group_msg(aim,content)
            bot.cqapi.send_group_msg(aim,ans)
            bot.cqapi.send_group_msg(aim,"%s" % record(file='file:///' + path))
            logging.info('发送成功！')
            return
        if '#登录空间' in message.message:
            print('开始登录空间')
            waifu.qzonebot.login()
            return
        if '#连接vits' in message.message:
            waifu.v=vits()
            return
        if '#发送语音' in message.message:
            text = message.message
            text= fanyi(text.replace('#发送语音',''))
            print(text)
            path=voice_vits(text=text)
            # time.sleep(5)
            path = path.replace("b'",'')
            path = path.replace("'",'')
            print(path)
            message.sender.send_message("%s" % record(file='file:///' + path))
            message.sender.send_message(text)
            # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
            
            logging.info('发送语音，文件目录是'+path)
            return
        if '#发送说说' in message.message:
            if message.sender.id!=169829974:
                message.sender.send_message('你在想什么呢，让我给你发说说？')
                return
            logging.info(f'{message.message}')
            waifu.ss(message)
            return
        if '#关闭群聊' in message.message:
            ql=False
            message.sender.send_message('关闭群聊成功')
            return
        if '#打开群聊' in message.message:
            ql=True
            message.sender.send_message('打开群聊成功')
            return
        if 'CQ' in message.message:
            logging.info(f'{message.message}')
        if group and (not ql):
            return
        try:
            # text=''
            # waifu.brain.think('/reset')
            if message.sender.id!=169829974:
                reply = waifu.stranger(message)
            else: 
                reply = str(waifu.ask(message.message))
            
                        # emotion = waifu.analyze_emotion(st)
                        # tts.speak(st, emotion)
                        # file_path = './output.wav'
                        # abs_path = os.path.abspath(file_path)
                        # mtime = os.path.getmtime(file_path)
                        # local_time = time.localtime(mtime)
                        # time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
                        # message.sender.send_message("%s" % record(file='file:///' + abs_path))
                        # logging.info(f'发送语音({emotion} {time_str}): {st}')
            if send_text:
                nlp = SnowNLP(reply)
                print('NLP Success')
                sentences=nlp.sentences
                if sdv:
                    if not fenju:
                        ans=fanyi(reply)
                        text = ans
                        print(text)
                        path=voice_vits(text=text)
                        # time.sleep(5)
                        path = path.replace("b'",'')
                        path = path.replace("'",'')
                        print(path)
                        message.sender.send_message(text)
                        message.sender.send_message(reply)
                        time.sleep(0.5)
                        message.sender.send_message("%s" % record(file='file:///' + path))
                        
                        # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
                        
                        logging.info('发送语音，文件目录是'+path)
                    else:
                        for st in sentences:
                            time.sleep(0.5)
                            if st == '' or st == ' ':
                                continue
                            
                            ans=waifu.fanyi(st)
                            text = ans
                            print(text)
                            path=voice_vits(text=text)
                            # time.sleep(5)
                            path = path.replace("b'",'')
                            path = path.replace("'",'')
                            print(path)
                            message.sender.send_message(text)
                            message.sender.send_message(st)
                            message.sender.send_message("%s" % record(file='file:///' + path))
                            
                            # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
                            
                            logging.info('发送语音，文件目录是'+path)
                elif send_text:
                    for st in sentences:
                            time.sleep(0.5)
                            if st == '' or st == ' ':
                                continue
                            message.sender.send_message(st)
                            logging.info(f'发送信息: {st}')
                            time.sleep(0.5)
            
            file_name = waifu.finish_ask(reply,message.sender.nickname)
            if not file_name == '':
                file_path = './presets/emoticon/' + file_name
                abs_path = os.path.abspath(file_path)
                message.sender.send_message("%s" % image(file='file:///' + abs_path))
            time.sleep(0.5)
            # waifu.brain.think('/reset 请忘记之前的对话')
        except Exception as e:
            logging.error(e)
    def on_group_msg_nonstream(message:Message):
        if message.sender.id != 169829974:
            return
        logging.info(f'收到群聊信息{message.message}')
        process(message=message,group=True)
        return
    def on_group_msg(message: Message):
        return
    def on_private_msg(message: Message):
        if '#发送说说' in message.message:
            waifu.ss(message)
        if 'CQ' in message.message:
            return
        callback.set_sender(message.sender)
        try:
            waifu.ask(message.message)
        except Exception as e:
            logging.error(e)

    def on_private_msg_nonstream(message: Message):
        process(message=message)
        # global sdv
        # global fenju
        # global last_pic
        # if '#upscale' in message.message:
        #     print('upscaling')
        #     target=message.message.replace('#upscale ','')
        #     url=upscale(last_pic,int(target))
        #     print(url)
        #     if url != '':
        #         print('绘图成功')
        #     else:
        #         print('failed')
        #         message.sender.send_message('failed')
        #         return
        #     # print(url)

        #     # urllib.request.urlretrieve(url=url,filename='./mid.png')
        #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        #     r = requests.get(url=url, headers=headers)

        #     # print(r.text)

        #     with open(r'C:\Users\Administrator\Desktop\AnimeWaifu\mid.png','wb') as f:
        #         f.write(r.content)
        #     message.sender.send_message('Success')
        #     message.sender.send_message(image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
        #     return
        # if '#发送群聊画图' in message.message:
        #     print('发送群聊画图')
        #     cmd=message.message.replace('#单独发送语音','')
        #     print(cmd)
        #     cmds=cmd.split('|')
        #     prompt=cmd[1]
        #     aim=cmd[0]
        #     print('进入绘图')
        #     last_pic,url=sendprompt(prompt)
        #     print(url)
        #     if url != '':
        #         print('绘图成功')
        #     print(url)
        #     # urllib.request.urlretrieve(url=url,filename='./mid.png')
        #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        #     r = requests.get(url=url, headers=headers)
        #     # print(r.text)
        #     with open(r'C:\Users\Administrator\Desktop\AnimeWaifu\mid.png','wb') as f:
        #         f.write(r.content)
        #     bot.cqapi.send_group_msg(int(aim),image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
        #     return
        # if '#绘图' in message.message:
        #     print('进入绘图')
        #     prompt = message.message.replace('#绘图 ','')
        #     last_pic,url=sendprompt(prompt)
        #     print(url)
        #     if url != '':
        #         print('绘图成功')
        #     print(url)

        #     # urllib.request.urlretrieve(url=url,filename='./mid.png')
        #     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        #     r = requests.get(url=url, headers=headers)

        #     # print(r.text)

        #     with open(r'C:\Users\Administrator\Desktop\AnimeWaifu\mid.png','wb') as f:
        #         f.write(r.content)
        #     message.sender.send_message(image('file:///C:/Users/Administrator/Desktop/AnimeWaifu/mid.png'))
        #     return

        # if '#更改包' in message.message:
        #     pkg=message.message.replace('#更改包','')
        #     waifu.v.change('model='+pkg)
        #     print('更改包成功')
        #     message.sender.send_message('更改包成功')
        #     return
        # if '#更改模型' in message.message:
        #     model=message.message.replace('#更改模型','')
        #     waifu.v.change('speaker='+model)
        #     print('更改模型成功')
        #     message.sender.send_message('更改模型成功')
        #     return
        # if '#关闭语音' in message.message:
        #     sdv=False
        #     message.sender.send_message('关闭语音成功')
        #     return
        # if '#打开语音' in message.message:
        #     sdv=True
        #     message.sender.send_message('打开语音成功')
        #     return
        # if '#关闭分句' in message.message:
        #     fenju=False
        #     message.sender.send_message('关闭分句成功')
        #     return
        # if '#打开分句' in message.message:
        #     fenju = True
        #     message.sender.send_message('打开分句成功')
        #     return
        # if '#单独发送语音' in message.message:
        #     print('开始单独发送语音')
        #     cmd=message.message.replace('#单独发送语音','')
        #     print(cmd)
        #     cmds=cmd.split('|')
        #     aim=int(cmds[0])
        #     content=cmds[1]
        #     print(aim)
        #     print(content)
        #     ans=fanyi(content)
        #     print(ans)
        #     path=voice_vits(text=ans)
        #     # time.sleep(5)
        #     path = path.replace("b'",'')
        #     path = path.replace("'",'')
        #     print(path)
        #     bot.cqapi.send_private_msg(aim,content)
        #     bot.cqapi.send_private_msg(aim,ans)
        #     bot.cqapi.send_private_msg(aim,"%s" % record(file='file:///' + path))
        #     logging.info('发送成功！')
        #     return
        # if '#发送群聊语音' in message.message:
        #     print('开始发送群聊语音')
        #     cmd=message.message.replace('#发送群聊语音','')
        #     print(cmd)
        #     cmds=cmd.split('|')
        #     aim=int(cmds[0])
        #     content=cmds[1]
        #     print(aim)
        #     print(content)
        #     ans=fanyi(content)
        #     print(ans)
        #     path=voice_vits(text=ans)
        #     # time.sleep(5)
        #     path = path.replace("b'",'')
        #     path = path.replace("'",'')
        #     print(path)
        #     bot.cqapi.send_group_msg(aim,content)
        #     bot.cqapi.send_group_msg(aim,ans)
        #     bot.cqapi.send_group_msg(aim,"%s" % record(file='file:///' + path))
        #     logging.info('发送成功！')
        #     return
        # if '#登录空间' in message.message:
        #     print('开始登录空间')
        #     waifu.qzonebot.login()
        #     return
        # if '#连接vits' in message.message:
        #     waifu.v=vits()
        #     return
        # if '#发送语音' in message.message:
        #     text = message.message
        #     text=fanyi(text.replace('#发送语音',''))
        #     print(text)
        #     path=voice_vits(text=text)
        #     # time.sleep(5)
        #     path = path.replace("b'",'')
        #     path = path.replace("'",'')
        #     print(path)
        #     message.sender.send_message("%s" % record(file='file:///' + path))
        #     message.sender.send_message(text)
        #     # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
            
        #     logging.info('发送语音，文件目录是'+path)
        #     return
        # if '#发送说说' in message.message:
        #     if message.sender.id!=169829974:
        #         message.sender.send_message('你在想什么呢，让我给你发说说？')
        #         return
        #     logging.info(f'{message.message}')
        #     waifu.ss(message)
        #     return
        # if 'CQ' in message.message:
        #     logging.info(f'{message.message}')
            
        # try:
        #     # text=''
        #     waifu.brain.think('/reset')
        #     if message.sender.id!=169829974:
        #         reply = waifu.stranger(message)
        #     else: 
        #         reply = waifu.ask(message.message)
            
        #                 # emotion = waifu.analyze_emotion(st)
        #                 # tts.speak(st, emotion)
        #                 # file_path = './output.wav'
        #                 # abs_path = os.path.abspath(file_path)
        #                 # mtime = os.path.getmtime(file_path)
        #                 # local_time = time.localtime(mtime)
        #                 # time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        #                 # message.sender.send_message("%s" % record(file='file:///' + abs_path))
        #                 # logging.info(f'发送语音({emotion} {time_str}): {st}')
        #     if send_text:
        #         nlp = SnowNLP(reply)
        #         sentences=nlp.sentences
        #         if sdv:
        #             if not fenju:
        #                 ans=fanyi(reply)
        #                 text = ans
        #                 print(text)
        #                 path=voice_vits(text=text)
        #                 # time.sleep(5)
        #                 path = path.replace("b'",'')
        #                 path = path.replace("'",'')
        #                 print(path)
        #                 message.sender.send_message(text)
        #                 message.sender.send_message(reply)
        #                 time.sleep(0.5)
        #                 message.sender.send_message("%s" % record(file='file:///' + path))
                        
        #                 # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
                        
        #                 logging.info('发送语音，文件目录是'+path)
        #             else:
        #                 for st in sentences:
        #                     time.sleep(0.5)
        #                     if st == '' or st == ' ':
        #                         continue
                            
        #                     ans=fanyi(st)
        #                     text = ans
        #                     print(text)
        #                     path=voice_vits(text=text)
        #                     # time.sleep(5)
        #                     path = path.replace("b'",'')
        #                     path = path.replace("'",'')
        #                     print(path)
        #                     message.sender.send_message(text)
        #                     message.sender.send_message(st)
        #                     message.sender.send_message("%s" % record(file='file:///' + path))
                            
        #                     # message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
                            
        #                     logging.info('发送语音，文件目录是'+path)
        #         elif send_text:
        #             for st in sentences:
        #                     time.sleep(0.5)
        #                     if st == '' or st == ' ':
        #                         continue
        #                     message.sender.send_message(st)
        #                     logging.info(f'发送信息: {st}')
        #                     time.sleep(0.5)
            
        #     file_name = waifu.finish_ask(reply,message.sender.nickname)
        #     if not file_name == '':
        #         file_path = './presets/emoticon/' + file_name
        #         abs_path = os.path.abspath(file_path)
        #         message.sender.send_message("%s" % image(file='file:///' + abs_path))
        #     time.sleep(0.5)
        #     waifu.brain.think('/reset 请忘记之前的对话')
        # except Exception as e:
        #     logging.error(e)

    user = load_config()

    bot = cqapi.create_bot(
        group_id_list=[],
        user_id_list=user,
        options={
            "commandSign":"$"
        }
    )
    if callback is None:
        bot.on_private_msg = on_private_msg_nonstream
        bot.on_group_msg = on_group_msg_nonstream
    else:
        bot.on_private_msg = on_private_msg

    # TODO: 指令功能
    # def echo(commandData, message: Message):
    #     # 回复消息
    #     message.sender.send_message(" ".join(commandData))
    # 设置指令为 echo
    # bot.command(echo, "echo", {
    #     # echo 帮助
    #     "help": [
    #         "#echo - 输出文本"
    #     ],
    #     "type": "all"
    # })

    # def sendrecord(commandData,message:Message):
        
    #     if '#发送语音' in message.message:
    #         text = message.message
    #         ans=fanyi(text.replace('#发送语音',''))
    #         print(ans)
    #         path=voice_vits(text=ans)
    #         time.sleep(5)
    #         path = path.replace("b'",'')
    #         path = path.replace("'",'')
    #         print(path)
    #         # message.sender.send_message("%s" % record(file='file:///' + 'E:/ChatWaifu-API-main/output.wav'))
    #         message.sender.send_message(ans)
    #         message.sender.send_message("%s" % record(file='http://192.168.1.102/VITS/output.wav'))
            
    #         logging.info('发送语音，文件目录是'+path)
    #         return
    
    # bot.command(sendrecord,"#发送语音",{
    #     # sendrecord 帮助
    #     "help": [
    #         "#sendrecord - 输出文本"
    #     ],
    #     "type": "all"
    # })

    bot.start(go_cqhttp_path='./qqbot/')
    
