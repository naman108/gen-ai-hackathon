from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String
from . import db
class Patient(db.Model):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    msi = Column(String(45), nullable=False)
    f_name = Column(String(45), nullable=False)
    l_name = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    last_visit = Column(DateTime)
    address = Column(String(45), nullable=False)
    history = Column(String, nullable=True)