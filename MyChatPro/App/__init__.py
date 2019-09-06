import tornado.web
from App.urls import patterns
from App.settings import app_settings

#创建应用, 并设置了路由规则
def make_app():
    return tornado.web.Application(
        handlers = patterns,

        **app_settings,
    )