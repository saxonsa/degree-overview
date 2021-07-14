from sqlalchemy import Column, String, ForeignKey, Float
from .base import Base
from .student import Student


class Grade(Base):
    __tablename__ = 'grades'
    stuid = Column(String(20), ForeignKey(Student.stuid), nullable=False, primary_key=True)
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    ass_method = Column(String(50), unique=False, nullable=True, primary_key=True)
    partial_score = Column(Float, unique=False, nullable=True)
