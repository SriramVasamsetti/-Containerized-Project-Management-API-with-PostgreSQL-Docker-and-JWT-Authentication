from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from src.schemas.user import UserResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register(data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.login(data)
