from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
from uuid import uuid4

from ..db.database import get_db
from ..models import User
from ..schemas.auth import SignupRequest, LoginRequest, AuthResponse, UserResponse
from ..core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # Check if user with email already exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user = User(
        id=uuid4(),
        first_name=payload.first_name,
        last_name=payload.last_name,
        address=payload.address,
        phone=payload.phone,
        email=payload.email,
        service=payload.service,
        auth_provider=payload.auth_provider,
        password_hash=hash_password(payload.password),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    print("\n=== Login Attempt ===")
    print(f"Email: {payload.email}")
    print(f"Request received at: {datetime.now(timezone.utc).isoformat()}")
    
    try:
        # Debug: Check database connection
        db.execute(text("SELECT 1"))
        db.commit()
        print("Database connection: OK")
        
        # Find user
        user = db.query(User).filter(User.email == payload.email).first()
        
        if not user:
            print("ERROR: No user found with this email")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        print(f"User found - ID: {user.id}")
        print(f"Stored password hash: {user.password_hash[:20]}...")
        
        # Verify password
        try:
            is_password_valid = verify_password(payload.password, user.password_hash)
            print(f"Password verification result: {is_password_valid}")
            
            if not is_password_valid:
                print("ERROR: Password verification failed")
                # Debug: Try to re-hash the provided password to see if it matches
                temp_hash = hash_password(payload.password)
                print(f"New hash of provided password: {temp_hash[:20]}...")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
        except Exception as e:
            print(f"ERROR during password verification: {str(e)}")
            print(f"Password hash type: {type(user.password_hash)}")
            print(f"Provided password type: {type(payload.password)}")
            raise
            
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    
    # Update last login time
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    
    # Create access token
    access_token = create_access_token(subject=str(user.id))
    
    # Return both the token and user info
    return AuthResponse(
        access_token=access_token,
        user=user
    )
