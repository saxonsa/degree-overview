from sqlalchemy import Column, String, LargeBinary
from .base import Base
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import DebugMode
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __abstract__ = True
    nickname = Column(String(20), unique=True, nullable=True)
    _password = Column('password', String(100), unique=False, nullable=False)
    englishname = Column(String(100), unique=False, nullable=True)
    phone = Column(String(11), unique=True, nullable=True)
    email = Column(String(50), unique=True, nullable=True)
    avatar = Column(LargeBinary(length=2048), unique=False, nullable=True)
    program = Column(String(20), nullable=True)
    gender = Column(String(10), nullable=True)

    def __init__(self, nickname, password, englishname, phone, email, avatar, program, gender):
        self.nickname = nickname
        self._password = generate_password_hash(password)
        self.englishname = englishname
        self.phone = phone
        self.email = email
        self.avatar = avatar
        self.program = program
        self.gender = gender

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    # 生成token
    @staticmethod
    def generate_auth_token(id):
        """
        生成token
        :param id: 传入Id来生成token
        :return:
        """
        s = Serializer(DebugMode.SECRET_KEY, expires_in=DebugMode.TOKEN_EXPIRATION)
        token = s.dumps({"id": id}).decode('utf-8')
        return token

    def get_nickname(self):
        return self.nickname

    def get_englishname(self):
        return self.englishname

    def get_phone(self):
        return self.phone

    def get_email(self):
        return self.email

    def get_program(self):
        return self.program

    def get_gender(self):
        return self.gender
