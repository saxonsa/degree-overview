from sqlalchemy import Column, String, LargeBinary
from .base import Base


class File(Base):
    __tablename__ = 'file'
    name = Column(String(100), unique=True, nullable=True, primary_key=True)
    content = Column(LargeBinary(length=2048), unique=False, nullable=True)
