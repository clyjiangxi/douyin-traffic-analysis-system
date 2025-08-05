from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(64), nullable=False)
    douyin_id = Column(String(64), nullable=False, unique=True)
    fans_count = Column(Integer, default=0)
    avatar_url = Column(String(255))
    profile_url = Column(String(255))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class AdvertiserRequest(Base):
    __tablename__ = "advertiser_requests"
    id = Column(Integer, primary_key=True, index=True)
    advertiser = Column(String(64), nullable=False)
    product_type = Column(String(64))
    target_audience = Column(String(128))
    budget = Column(Integer)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(16), default="user")  # user/admin
    created_at = Column(DateTime, default=datetime.utcnow) 