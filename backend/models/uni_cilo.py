from sqlalchemy import Column, String, ForeignKey, Float, Integer
from .base import Base
from .student import Student


class Uni_CILO(Base):
    __tablename__ = 'unicilo'
    stuid = Column(String(20), ForeignKey(Student.stuid), primary_key=True)
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    cilo_index = Column(Integer, nullable=True, unique=False, primary_key=True)
    cilo_performance = Column(Float, nullable=True, unique=False)
