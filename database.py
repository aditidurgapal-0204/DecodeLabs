from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create the Database Vault File
SQLALCHEMY_DATABASE_URL = "sqlite:///./vault.db"

# 2. Establish Connection Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 3. Define the Blueprint User Schema
class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False) 
    age = Column(Integer, default=0) 
    is_active = Column(Boolean, default=True) 

# Helper to capture session requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()