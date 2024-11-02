from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    work_id = Column(Integer, ForeignKey("works.id"))
    work = relationship("WorkDB", backref="users")


class WorkDB(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    salary = Column(Integer)
