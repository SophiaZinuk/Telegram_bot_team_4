from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String)
    user_type: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    chat_id: Mapped[str] = mapped_column(Integer)
    applications: Mapped[List['Application']] = relationship()


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    application_type: Mapped[str] = mapped_column(String)
    application_status: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String)
    application_data: Mapped['ApplicationData'] = relationship(back_populates='application')
    creator: Mapped['User'] = relationship(back_populates='applications')


class ApplicationData(Base):
    __tablename__ = 'application_data'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_number: Mapped[str] = mapped_column(String)
    application_id: Mapped[int] = mapped_column(ForeignKey('applications.id'))
    application: Mapped['Application'] = relationship('Application', back_populates='application_data')
