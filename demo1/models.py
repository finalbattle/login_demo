# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = 'mysql+pymysql://root:@localhost:3306/demo1?charset=utf8'

engine = create_engine(db_url)
DBSession = sessionmaker(engine)
#db = DBSession()

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=text("curtime()"))
