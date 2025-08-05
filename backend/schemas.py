from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    nickname: str
    douyin_id: str
    fans_count: Optional[int] = 0
    avatar_url: Optional[str] = None
    profile_url: Optional[str] = None
    description: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    created_at: datetime
    reason: Optional[str] = None  # 新增推荐理由字段

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class AdvertiserRequestBase(BaseModel):
    advertiser: str
    product_type: Optional[str] = None
    target_audience: Optional[str] = None
    budget: Optional[int] = None
    description: Optional[str] = None

class AdvertiserRequestCreate(AdvertiserRequestBase):
    pass

class AdvertiserRequest(AdvertiserRequestBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

# 用户相关
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "user"

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None 