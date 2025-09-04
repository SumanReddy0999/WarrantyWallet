from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from uuid import UUID
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from .config import settings

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    subject: Union[str, UUID], 
    expires_minutes: Optional[int] = None,
    additional_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        subject: The subject of the token (usually user ID)
        expires_minutes: Token expiration time in minutes
        additional_data: Additional data to include in the token payload
    """
    expire_delta = timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + expire_delta
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(tz=timezone.utc),
        "type": "access"
    }
    
    if additional_data:
        to_encode.update(additional_data)
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token and return the payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get the current user from the JWT token
    """
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


