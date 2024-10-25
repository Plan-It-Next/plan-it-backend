from passlib.context import CryptContext


class PassVal:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(password: str) -> str:
        return PassVal.pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PassVal.pwd_context.verify(plain_password, hashed_password)