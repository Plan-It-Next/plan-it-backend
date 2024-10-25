import os
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from dotenv import load_dotenv


class AuthMiddleware:
    def __init__(self):
        load_dotenv()
        self.secret = os.getenv('JWT_SECRET_KEY')

    def is_valid_token(self, token: str):
        try:
            return jwt.decode(token, self.secret, algorithms=["HS256"], options={"verify_aud": False, "verify_iat": False})
        except Exception as e:
            print(str(e))
            return None  # Retorna None si el token no es válido

    async def authenticate(self, auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if not auth:
            print('not auth')
            raise HTTPException(status_code=401, detail='Unauthorized')
        if not self.is_valid_token(auth.credentials):
            raise HTTPException(status_code=401, detail='Unauthorized')

auth_middleware = AuthMiddleware()

async def require_authentication(auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return await auth_middleware.authenticate(auth)