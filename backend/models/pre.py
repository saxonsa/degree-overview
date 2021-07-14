from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base


class Pre(Base):
    __tablename__ = 'pre'
    post_course = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    post_cilo_index = Column(Integer, unique=False, nullable=False, default=None, primary_key=True)
    pre_course = Column(String(20), ForeignKey("courses.course_code"), primary_key=True)
    pre_cilo_index = Column(Integer, unique=False, nullable=False, default=None, primary_key=True)
    type = Column(Integer, unique=False, nullable=False, primary_key=True)
