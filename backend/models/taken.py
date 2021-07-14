from sqlalchemy import Column, String, ForeignKey, Float, Integer
from .base import Base
from .student import Student


class Taken(Base):
    __tablename__ = 'taken'
    stuid = Column(String(20), ForeignKey(Student.stuid), primary_key=True)
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    year = Column(String(20), nullable=True)
    semester = Column(Integer, nullable=True)
    total_score = Column(Float, nullable=True)