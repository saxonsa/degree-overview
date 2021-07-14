from sqlalchemy import Column, String, Integer
from .user import User


class Lecturer(User):
    __tablename__ = 'lecturers'
    staffid = Column(String(20), primary_key=True, nullable=False)
    designAuth = Column(Integer, unique=False, nullable=True, default=0)
    staffHonor = Column(String(20), unique=False, nullable=True)

    def __init__(self, nickname, password, englishname, phone, email, avatar, program, gender, staffid, designAuth, staffHonor):
        super(Lecturer, self).__init__(nickname, password, englishname, phone, email, avatar, program, gender)
        self.staffid = staffid
        self.designAuth = designAuth
        self.staffHonor = staffHonor

    def get_design_auth(self):
        return self.designAuth

    def get_staffid(self):
        return self.staffid
