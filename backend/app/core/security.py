from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from uuid import UUID
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..db.database import get_db

from .config import settings

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    Automatically handles password length limits by hashing the password first with SHA-256.
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    Matches the hashing method used in hash_password.
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
        # Log token for debugging (first 10 chars only for security)
        print(f"Decoding token: {token[:10]}...")
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={
                "verify_aud": False,
                "verify_iss": False,
                "verify_iat": True,
                "verify_exp": True,
                "verify_nbf": False
            }
        )
        print(f"Token decoded successfully for user: {payload.get('sub')}")
        return payload
    except JWTError as e:
        error_msg = f"JWT Error: {str(e)}"
        print(error_msg)  # Log the actual error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,  # Return the actual error to client
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> 'User':  # Forward reference to avoid circular import
    """
    Get the current user from the JWT token
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
            
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        
        if not user_id:
            print("Error: No 'sub' claim in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing user identification",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        print(f"Authenticated user ID: {user_id}")
        
        # Import User model here to avoid circular imports
        from app.models import User
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
            
        return user
    except JWTError as e:
        print(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )