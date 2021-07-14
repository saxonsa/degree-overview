from sqlalchemy import Column, String, ForeignKey, Float, Integer
from .base import Base


class Semes_CILO(Base):
    __tablename__ = 'semescilo'
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    year = Column(String(20), nullable=False, primary_key=True)
    semester = Column(Integer, nullable=False, primary_key=True)
    cilo_index = Column(Integer, nullable=False, primary_key=True)
    semes_cilo_score = Column(Float, nullable=True, unique=False)