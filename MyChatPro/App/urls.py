# urls.py: 存放路由配置
from tornado.web import url

from App.views import *

patterns = [
    url(r'/orm/', ORMHandler, name='orm'),
    url(r'/clear/', ClearCookieHandler, name='clear'),

    url(r'/index/',IndexHandler,name='index'),
    url(r'/chat/',ChatHandler,name='chat'),
    url(r'/chatroom/',ChatRoomHandler,name='chatroom'),
    url(r'/login/',LoginHandler,name='login'),
    url(r'/logout/',LogoutHandler,name='logout'),
    url(r'/register/',RegisterHandler,name='register'),
]