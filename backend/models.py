from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer,primary_key=True)
    player_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())