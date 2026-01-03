from sqlalchemy import Column, Float, Integer

from app.db import Base


class Data(Base):
    __tablename__ = 'data_points'
    id = Column(Integer, primary_key=True)
    category = Column(Integer)
    width = Column(Float)
    height = Column(Float)
    length = Column(Float)
    weight = Column(Float)
