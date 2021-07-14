from sqlalchemy import Column, String, Integer
from .base import Base, db
from .pre import Pre


class Course(Base):
    __tablename__ = 'courses'
    course_code = Column(String(20), primary_key=True)
    course_name = Column(String(100), unique=True, nullable=False)
    course_type = Column(String(20), unique=False, nullable=True)
    department = Column(String(50), unique=False, nullable=True)
    unit = Column(Integer, unique=False, nullable=True)
    year = Column(String(5), unique=False, nullable=True)

    post = db.relationship("Pre",
                           foreign_keys=[Pre.post_course],
                           backref=db.backref("post_c", lazy="joined"),
                           lazy="dynamic",
                           cascade="all, delete-orphan")

    pre = db.relationship("Pre",
                          foreign_keys=[Pre.pre_course],
                          backref=db.backref("pre_c", lazy="joined"),
                          lazy="dynamic",
                          cascade="all, delete-orphan")
