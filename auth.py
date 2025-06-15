from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key_here"  # غيرها لمفتاح سري قوي، خليه سر خاص بيك
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # مدة صلاحية التوكن بالدقائق

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
