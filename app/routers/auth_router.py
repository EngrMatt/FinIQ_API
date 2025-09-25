from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user import User        
from app.core.security import hash_password, verify_password, create_access_token
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        if existing.is_active:
            raise HTTPException(status_code=400, detail="Email already registered and active")
        else:
            # 使用者還沒驗證過，可以重新發驗證信
            existing.hashed_password = hash_password(user.password)
            db.add(existing)
            db.commit()
            db.refresh(existing)
            # TODO: send_verification_email(existing.email, token)
            return existing

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=False  # 預設未啟用，等驗證信
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # TODO: send_verification_email(new_user.email, token)

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
