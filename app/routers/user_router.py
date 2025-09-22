from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService

# 在這裡直接設定 prefix 與 tags
router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
