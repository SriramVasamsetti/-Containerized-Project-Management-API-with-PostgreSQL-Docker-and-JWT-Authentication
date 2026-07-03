from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.core.security import get_password_hash, verify_password, create_access_token
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> User:
        existing_user = self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(data.password)
        new_user = User(email=data.email, password_hash=hashed_password)
        return self.user_repo.create(new_user)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(subject=user.id)
        return TokenResponse(access_token=access_token, token_type="bearer")
