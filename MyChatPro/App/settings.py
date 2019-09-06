# settings.py: 项目配置
import os

from tornado.options import define,options

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
define('port' , default=80 , type=int)
define('debug' , default=True , type=bool)


app_settings = {
    'debug' : options.debug,
    'template_path' : os.path.join(BASE_DIR,'templates'),
    'static_path' : os.path.join(BASE_DIR,'static'),
}
