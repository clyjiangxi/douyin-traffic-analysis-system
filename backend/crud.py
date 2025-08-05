from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account

def get_advertiser_request(db: Session, request_id: int):
    return db.query(models.AdvertiserRequest).filter(models.AdvertiserRequest.id == request_id).first()

def get_advertiser_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AdvertiserRequest).offset(skip).limit(limit).all()

def create_advertiser_request(db: Session, req: schemas.AdvertiserRequestCreate):
    db_req = models.AdvertiserRequest(**req.dict())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

def delete_advertiser_request(db: Session, request_id: int):
    db_req = db.query(models.AdvertiserRequest).filter(models.AdvertiserRequest.id == request_id).first()
    if db_req:
        db.delete(db_req)
        db.commit()
    return db_req

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 