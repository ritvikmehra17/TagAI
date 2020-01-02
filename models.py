
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()
engine = db.create_engine('sqlite:///database/tagAi.sqlite')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column( Integer, primary_key=True)
    username =Column( String(64),nullable=False)
    email = Column( String(64),nullable=False, unique=True)
    password = Column( String(64),nullable=False)
    created = Column(String(32), default=datetime.now())


class Upload(Base):
    __tablename__ = 'uploads'
    id = Column( Integer, primary_key=True)
    image = Column( String(64),nullable=False, unique=False)
    lastupload = Column(String(32), default=datetime.now())





