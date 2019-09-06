# views.py: 存放类视图
#   存放RequestHandler
import re

import tornado.web
import tornado.websocket

from utils.conn import session
from .models import *
import hashlib


# 创建用户表
class ORMHandler(tornado.web.RequestHandler):
    def get(self):
        create_db()
        self.write("create database success...")

# 首页
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

# 聊天页面
class ChatHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('chat.html')

# 登录
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('passwd')
        # password = my_md5(password)

        users = session.query(User).filter_by(username=username, password=password)
        if users.count() == 0 :
            self.write('请先注册再登录...')
            return

        if users.first().islogin == True:
            self.write('%s已经登录...'%username)
            return

        users.first().islogin = True
        session.commit()

        self.set_cookie('username', username)
        self.redirect(self.reverse_url('chat'))
        # self.render('chat.html',username = username)

# 注册
class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
       self.render('register.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('passwd')
        # password = my_md5(password)
        #
        # if not re.match('^\w{6,20}$', username):
        #     self.write("用户名不合法")
        #     return
        # if not re.match('^\w{6,20}$', password):
        #     self.write("密码不合法")
        #     return

        # 判断用户是否存在
        users = session.query(User).filter_by(username=username,password= password)
        if users.count() > 0:
            self.write("用户已注册")
            return

        # 添加用户
        user = User()
        user.username = username
        user.password = password

        try:
            session.add(user)
            session.commit()
        except:
            session.rollback()
            session.flush()
            self.write('注册失败')
        else:
            self.redirect(self.reverse_url('login'))

class ChatRoomHandler(tornado.websocket.WebSocketHandler):

    online_users = []

    def open(self, *args: str, **kwargs: str):
        print('open')

        username = self.get_cookie('username')
        # 当有新用户连接时, 会加入到online_users中
        self.online_users.append(self)
        # 当新用户加入到聊天室时, 会显示用户进入聊天室
        for user in self.online_users:
            user.write_message('%s进入聊天室' %username)

    # 当客户端发送数据给我时, 就会调用
    def on_message(self,message):
        print('message:',message)

        # 获取发送信息到服务器的用户名
        username = self.get_cookie('username')

        # 发送数据给所有在线的用户
        for user in self.online_users:
            user.write_message('[%s]:%s'%(username,message))

    # 断开连接时调用
    def on_close(self):
        username = self.get_cookie('username')

        users = session.query(User).filter_by(username = username)
        users.first().islogin = False
        session.commit()
        print('close')
        self.clear_cookie('username')
        # self.write("您已退出聊天...")
        self.online_users.remove(self)
# 下线
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('logout.html')       # self.redirect(self.reverse_url('logout'))

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('passwd')

        users = session.query(User).filter_by(username=username, password=password)
        if users.count() == 0 :
            self.write('账号不存在...')
            return

        users.first().islogin = False
        session.commit()

        self.redirect(self.reverse_url('index'))


class ClearCookieHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie('username')
        self.write('clear cookie...')

# md5: 不可逆(只能加密, 不能解密)
# RSA: 非对称加密, 私钥和公钥
   # 16进制32位密文




