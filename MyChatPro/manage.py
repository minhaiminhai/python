# 接收命令行参数 ,并启动项目
import tornado.ioloop
from tornado.options import parse_command_line, options
from App import make_app

# 接收命令行参数
parse_command_line()

# 启动项目
app = make_app()
app.listen(options.port)
tornado.ioloop.IOLoop.current().start()