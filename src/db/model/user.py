from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    user_type = Column(String)
    phone_number = Column(String)
    chat_id = Column(Integer)
