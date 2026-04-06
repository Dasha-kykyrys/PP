import hashlib

def hash_password(password: str) -> str:
    """
    Хэширование пароля
    """
    hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверка пароля на соответствие хэшу
    """
    return hash_password(password) == hashed_password
