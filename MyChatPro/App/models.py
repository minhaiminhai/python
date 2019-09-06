# models.py
#   这里写模型
#   模型: 数据库表
from sqlalchemy import Column, Integer, String, Boolean

from utils.conn import Base
import hashlib


def create_db():
    Base.metadata.create_all()

class User(Base):
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True)
    password = Column(String(40))
    islogin = Column(Boolean, default=False)


# def my_md5(s):
#     m = hashlib.md5()
#     m.update(s.encode())
#     return m.hexdigest
