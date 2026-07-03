from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import database

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: int
    email: str
    age: int
    is_active: bool

    class Config:
        from_attributes = True

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(database.get_db)):
    if user_data.age < 0:
        raise HTTPException(status_code=400, detail="Age must be greater than or equal to 0")

    existing_user = db.query(database.DBUser).filter(database.DBUser.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The Vault Breach: Email already exists.")
    
    db_user = database.DBUser(email=user_data.email, age=user_data.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(database.get_db)):
    return db.query(database.DBUser).all()