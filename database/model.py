from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Snippet(Base):
    __tablename__ = "snippers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, datetime.utcnow, onupdate=datetime.utcnow)