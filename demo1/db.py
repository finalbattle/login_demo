# coding: utf-8

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'demo1'
USERNAME = 'root'
PASSWORD = ''

db_url = f'mysql://{USERNAME}:{PASSWORD}@{HOTSNAME}:{PORT}/{DATABASE}?charset=utf-8'

engine = create_engine(db_url)

Base = declarative_base(bind=engine)

DBSession = sessionmaker(engine)
dbsession = DBSession()
