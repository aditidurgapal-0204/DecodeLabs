import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

import database
import security

router = APIRouter()

# Read the signing key from our secure local environment variables (Slide 8)
SECRET_KEY = os.getenv("JWT_SECRET", "fallback_secret_for_local_dev")
ALGORITHM = "HS256"

# This updates the UI to show a clean, single-input Token box instead of the large OAuth2 form
security_scheme = HTTPBearer()

# --- DATA SCHEMAS ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    age: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- TOKEN GENERATION (Slide 6) ---
def create_access_token(data: dict):
    to_encode = data.copy()
    # Token expires 15 minutes after issuance
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- THE BOUNCER MIDDLEWARE (Slide 7) ---
def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security_scheme)):
    # HTTPBearer automatically extracts the raw token string from the Authorization header
    token = cred.credentials
    try:
        # Crack open the token and mathematically verify its signature
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims.")
        return email
    except jwt.PyJWTError:
        # Slide 7 Matrix: 401 Unauthorized means token is missing, forged, or expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="I don't know who you are. Your token is missing, forged, or expired.",
        )

# --- 1. POST -> REGISTER: Hash and Save ---
@router.post("/register", status_code=201)
def register(user_data: UserRegister, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing = db.query(database.DBUser).filter(database.DBUser.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")
    
    # 🚨 HASH PASSWORDS BEFORE SAVING (Slide 3)
    hashed_password = security.hash_password(user_data.password)
    
    # Save user instance details to your database vault
    new_user = database.DBUser(email=user_data.email, age=user_data.age)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully! Password safely hashed via Argon2id."}

# --- 2. POST -> LOGIN: Issue VIP Token ---
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(database.get_db)):
    # Look up the user using the clean JSON email schema fields
    user = db.query(database.DBUser).filter(database.DBUser.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    # Generate token matching user email
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 3. GET -> PROTECTED ROUTE: Requires Token ---
@router.get("/dashboard")
def view_dashboard(current_user: str = Depends(get_current_user)):
    return {
        "message": "Welcome to the Protected Executive Suite Dashboard!",
        "secret_data": "This data can only be viewed if you are wearing a valid VIP JWT Wristband.",
        "logged_in_as": current_user
    }