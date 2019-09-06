from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1.配置MYsql数据库的路径
# DB_URI = "数据库类型+驱动://数据库用户名:密码@IP:端口/数据库名称"
DB_URI = "mysql+pymysql://root:1234@127.0.0.1:3306/mychat"
# sqlite : 轻量级的数据库

# 2.创建数据库引擎对象
engine = create_engine(DB_URI)

# 3.创建模型基类
Base = declarative_base(engine)

# 4.创建session: 用来操作数据库中的数据
DBsession = sessionmaker(bind=engine)
session = DBsession()


