from fastapi import APIRouter, Depends
from src.middleware.auth_dependency import get_current_user
from src.models.user import User
from src.schemas.user import UserResponse

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
