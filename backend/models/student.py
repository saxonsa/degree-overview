from sqlalchemy import Column, String, Integer
from .user import User


class Student(User):
    __tablename__ = 'students'
    stuid = Column(String(20), primary_key=True, nullable=False)
    register_year = Column(Integer, nullable=False)

    def __init__(self, nickname, password, englishname, phone, email, avatar, program, gender, stuid, register_year):
        super(Student, self).__init__(nickname, password, englishname, phone, email, avatar, program, gender)
        self.stuid = stuid
        self.register_year = register_year

    def get_student_id(self):
        return self.stuid
