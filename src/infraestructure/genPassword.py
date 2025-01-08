from src.infraestructure.password_validator import PassVal

hashed_password = PassVal.get_password_hash("password123")
print(hashed_password)
