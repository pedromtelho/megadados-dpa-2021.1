from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

USER = os.getenv('MEGADADOS_APS_USER')
PASSWORD = os.getenv('MEGADADOS_APS_USER_PASSWORD')
SERVER = os.getenv('MEGADADOS_APS_SERVER')
DB = os.getenv('MEGADADOS_APS_DB')

SQLALCHEMY_DATABASE_URL = 'mysql://megadados2021:Megadados2021!@localhost/aps'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
