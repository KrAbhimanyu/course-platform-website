from sqlalchemy import Column, Integer, String
from app.db import Base

class Course(Base):
    _tablename_ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)
    video_url = Column(String)