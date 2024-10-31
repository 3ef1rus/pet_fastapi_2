from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,index=True)
    age = Column(Integer)
    works = relationship("Work", backref="user")


class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    salary = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))