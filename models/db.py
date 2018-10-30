from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

HOSTNAME = 'localhost'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'qwe123'
DATABASES = 'tanzhou'


db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOSTNAME,PORT,DATABASES
)

engine = create_engine(db_url)
DBSession = sessionmaker(bind=engine)

Base = declarative_base(engine)
