from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    subjects = relationship('Subject', back_populates='teacher')
