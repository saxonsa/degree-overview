from sqlalchemy import Column, String, ForeignKey, Float
from .base import Base


class Assessment(Base):
    __tablename__ = 'assessment'
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    method = Column(String(50), unique=False, nullable=True, primary_key=True)
    percentage = Column(Float, unique=False, nullable=True)
    cilostr = Column(String(20), unique=False, nullable=True)
    year = Column(String(5), unique=False, nullable=True, primary_key=True)
