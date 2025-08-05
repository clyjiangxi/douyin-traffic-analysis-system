from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import random, string, datetime
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta
from fastapi import status, Security
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

SECRET_KEY = "supersecretkey1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        role: str = payload.get("role", "user")
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_admin_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限，仅管理员可操作")
    return current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(json_encoders={datetime.datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")})

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc) or "服务器内部错误"})

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(FastAPIRequestValidationError)
def validation_exception_handler(request: Request, exc: FastAPIRequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# 账号API
@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, account)

@app.get("/accounts/")
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    total = db.query(models.Account).count()
    items = crud.get_accounts(db, skip=skip, limit=limit)
    return {"total": total, "items": items}

@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.delete("/accounts/{account_id}", response_model=schemas.Account)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.delete_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    for k, v in account.dict().items():
        setattr(db_account, k, v)
    db.commit()
    db.refresh(db_account)
    return db_account

# 广告主需求API
@app.post("/advertiser_requests/", response_model=schemas.AdvertiserRequest)
def create_advertiser_request(req: schemas.AdvertiserRequestCreate, db: Session = Depends(get_db)):
    return crud.create_advertiser_request(db, req)

@app.get("/advertiser_requests/")
def read_advertiser_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    total = db.query(models.AdvertiserRequest).count()
    items = crud.get_advertiser_requests(db, skip=skip, limit=limit)
    return {"total": total, "items": items}

@app.get("/advertiser_requests/{request_id}", response_model=schemas.AdvertiserRequest)
def read_advertiser_request(request_id: int, db: Session = Depends(get_db)):
    db_req = crud.get_advertiser_request(db, request_id)
    if db_req is None:
        raise HTTPException(status_code=404, detail="Advertiser request not found")
    return db_req

@app.delete("/advertiser_requests/{request_id}", response_model=schemas.AdvertiserRequest)
def delete_advertiser_request(request_id: int, db: Session = Depends(get_db)):
    db_req = crud.delete_advertiser_request(db, request_id)
    if db_req is None:
        raise HTTPException(status_code=404, detail="Advertiser request not found")
    return db_req

@app.put("/advertiser_requests/{request_id}", response_model=schemas.AdvertiserRequest)
def update_advertiser_request(request_id: int, req: schemas.AdvertiserRequestCreate, db: Session = Depends(get_db)):
    db_req = db.query(models.AdvertiserRequest).filter(models.AdvertiserRequest.id == request_id).first()
    if not db_req:
        raise HTTPException(status_code=404, detail="Advertiser request not found")
    for k, v in req.dict().items():
        setattr(db_req, k, v)
    db.commit()
    db.refresh(db_req)
    return db_req

@app.post("/generate_test_data/")
def generate_test_data(db: Session = Depends(get_db)):
    # 清空原有数据
    db.query(models.Account).delete()
    db.query(models.AdvertiserRequest).delete()
    db.commit()
    # 生成20条账号
    for i in range(20):
        acc = models.Account(
            nickname=f"达人{i+1}",
            douyin_id=f"dy{1000+i}",
            fans_count=random.randint(1000, 100000),
            avatar_url="",
            profile_url="",
            description="测试账号",
            created_at=datetime.datetime.utcnow()
        )
        db.add(acc)
    # 生成20条广告主需求
    for i in range(20):
        req = models.AdvertiserRequest(
            advertiser=f"广告主{i+1}",
            product_type=random.choice(["美妆", "数码", "服饰", "美食", "母婴"]),
            target_audience=random.choice(["18-24女性", "25-34男性", "学生", "宝妈", "上班族"]),
            budget=random.randint(1000, 10000),
            description="测试需求",
            created_at=datetime.datetime.utcnow()
        )
        db.add(req)
    db.commit()
    return {"msg": "测试数据已生成"}

@app.get("/recommend_accounts/", response_model=List[schemas.Account])
def recommend_accounts(product_type: str = None, min_fans: int = 0, db: Session = Depends(get_db)):
    # 多条件加权推荐：粉丝数、产品类型、活跃度（假设有字段）
    accounts = db.query(models.Account).all()
    scored_accounts = []
    for acc in accounts:
        score = 0
        reasons = []
        # 粉丝数加权
        if acc.fans_count >= min_fans:
            score += (acc.fans_count - min_fans) / 1000
            reasons.append(f"粉丝数高于{min_fans}")
        else:
            reasons.append(f"粉丝数低于{min_fans}")
        # 产品类型加权（假设账号有 product_type 字段，否则跳过）
        if product_type and hasattr(acc, 'product_type'):
            if acc.product_type == product_type:
                score += 10
                reasons.append("产品类型完全匹配")
            else:
                reasons.append("产品类型不匹配")
        # 活跃度加权（假设有 acc.active_score 字段，否则跳过）
        if hasattr(acc, 'active_score'):
            score += acc.active_score
            reasons.append(f"活跃度分{acc.active_score}")
        scored_accounts.append({
            'account': acc,
            'score': score,
            'reason': '，'.join(reasons)
        })
    # 按分数排序，取前5
    scored_accounts.sort(key=lambda x: x['score'], reverse=True)
    # 返回账号和推荐理由
    result = []
    for item in scored_accounts[:5]:
        acc = item['account']
        acc.reason = item['reason']  # 动态加字段
        result.append(acc)
    return result

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return crud.create_user(db, user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.User)
def get_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user 