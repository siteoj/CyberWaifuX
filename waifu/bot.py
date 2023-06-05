import waifu.qzone.login
import waifu.qzone.model
import waifu.qzone.publisher
import logging
import re

class qzonebot():
    def __init__(self) -> None:
        self.qzone_login=waifu.qzone.login.QzoneLoginManager()
        self.cookies = self.qzone_login.login_via_qrcode()
        print("使用提供的cookie登录QQ空间失败,尝试使用二维码登录")
        self.cookie_str=''
        for k in self.cookies:
            self.cookie_str += "{}={};".format(k, self.cookies[k])
        print(self.cookie_str)
        print('\n'+'1')
        self.qzone_oper = waifu.qzone.model.QzoneOperator(int(str(self.cookies['uin']).replace("o", "")),
                                                       self.cookie_str)
        
        pass
    def send_emotion(self,str= ''):
        flag=0
        flag=self.qzone_oper.publish_emotion(str)
        if flag==0:
            logging.info(f'发送失败')
        else :
            logging.info(f'发送成功')
    def keepalive(self):
        self.qzone_oper.__keepalive_cookie(self.qzone_oper)
    def checkalive(self):
        self.qzone_oper.check_alive(self.qzone_oper)
    def store(self):
        config_file = open('config.py', encoding='utf-8', mode='r+')
        config_str = config_file.read()
        config_str = re.sub(r'qzone_cookie = .*', 'qzone_cookie = \'{}\''.format(self.cookie_str), config_str)
        config_file.seek(0)
        config_file.write(config_str)
        config_file.close()

        
    