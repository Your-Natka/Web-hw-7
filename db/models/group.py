from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    students = relationship('Student', back_populates='group')
