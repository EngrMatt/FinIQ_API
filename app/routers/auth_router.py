from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user import User        
from app.core.security import hash_password, verify_password, create_access_token
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email, User.is_active == True).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email 已被註冊")

    pending = db.query(User).filter(User.email == user.email, User.is_active == False).first()
    if pending:
        pending.hashed_password = hash_password(user.password)
        db.add(pending)
        db.commit()
        db.refresh(pending)
        new_user = pending
    else:
        new_user = User(email=user.email, hashed_password=hash_password(user.password), is_active=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.is_active == True).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/admin/activate/{user_id}")
def activate_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    return {"message": "User activated"}

