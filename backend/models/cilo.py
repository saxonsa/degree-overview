from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float
from .base import Base


class CILO(Base):
    __tablename__ = 'cilos'
    course_code = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    index = Column(Integer, unique=False, nullable=True, primary_key=True)
    content = Column(Text, unique=False, nullable=True)
    avg_score = Column(Float, unique=False, nullable=True)
