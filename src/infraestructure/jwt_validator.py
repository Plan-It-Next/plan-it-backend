import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, status
from src.domain.Repository.user_repository import UserRepository
from src.infraestructure.password_validator import PassVal

user_repo = UserRepository()
pass_val = PassVal()

class JwtVal:
    def __init__(self):
        load_dotenv()
        self.secret_key = os.getenv('JWT_SECRET_KEY')
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str):
        user = await user_repo.get_user_by_email(email)
        print(user)
        if user and PassVal.verify_password(password, user.password):
            return user
        return None


    async def login(self, email, password):
        user = await self.authenticate_user(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        # Crear el JWT Token
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.email},  # Incluir el email en el token
            expires_delta=access_token_expires
        )

        # Devolver el token y los detalles del usuario
        return {"access_token": access_token, "token_type": "bearer", "user": user}