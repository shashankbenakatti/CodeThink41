from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os

# Database setup
SQLITE_DATABASE_URL = "sqlite:///./snippets.db"
engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    user_str_id = Column(String, primary_key=True, index=True)

class Snippet(Base):
    __tablename__ = "snippets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_str_id = Column(String, index=True)
    snippet_name = Column(String, index=True)
    language = Column(String)
    code_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response
class SnippetCreate(BaseModel):
    snippet_name: str
    language: str
    code_content: str

class SnippetResponse(BaseModel):
    snippet_name: str
    language: str
    code_content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SnippetSummary(BaseModel):
    snippet_name: str
    language: str
    updated_at: datetime
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(
    title="Code Snippets Manager",
    description="Backend service for managing personal code snippets",
    version="1.0.0"
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to ensure user exists
def ensure_user_exists(user_str_id: str, db: Session):
    user = db.query(User).filter(User.user_str_id == user_str_id).first()
    if not user:
        user = User(user_str_id=user_str_id)
        db.add(user)
        db.commit()
    return user

@app.get("/")
def read_root():
    return {"message": "Code Snippets Manager API", "version": "1.0.0"}

@app.post("/users/{user_str_id}/snippets", response_model=SnippetResponse)
def create_or_update_snippet(
    user_str_id: str,
    snippet_data: SnippetCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update a code snippet for a user.
    If a snippet with the same name exists, it will be updated.
    """
    # Ensure user exists
    ensure_user_exists(user_str_id, db)
    
    # Check if snippet already exists
    existing_snippet = db.query(Snippet).filter(
        Snippet.user_str_id == user_str_id,
        Snippet.snippet_name == snippet_data.snippet_name
    ).first()
    
    if existing_snippet:
        # Update existing snippet
        existing_snippet.language = snippet_data.language
        existing_snippet.code_content = snippet_data.code_content
        existing_snippet.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_snippet)
        return existing_snippet
    else:
        # Create new snippet
        new_snippet = Snippet(
            user_str_id=user_str_id,
            snippet_name=snippet_data.snippet_name,
            language=snippet_data.language,
            code_content=snippet_data.code_content
        )
        db.add(new_snippet)
        db.commit()
        db.refresh(new_snippet)
        return new_snippet

@app.get("/users/{user_str_id}/snippets/{snippet_name}", response_model=SnippetResponse)
def get_snippet(
    user_str_id: str,
    snippet_name: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific named snippet for a user.
    Returns 404 if snippet doesn't exist.
    """
    snippet = db.query(Snippet).filter(
        Snippet.user_str_id == user_str_id,
        Snippet.snippet_name == snippet_name
    ).first()
    
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    return snippet

@app.get("/users/{user_str_id}/snippets", response_model=List[SnippetSummary])
def list_user_snippets(
    user_str_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all snippet names and languages for a user.
    """
    snippets = db.query(Snippet).filter(
        Snippet.user_str_id == user_str_id
    ).all()
    
    return snippets

@app.delete("/users/{user_str_id}/snippets/{snippet_name}")
def delete_snippet(
    user_str_id: str,
    snippet_name: str,
    db: Session = Depends(get_db)
):
    """
    Delete a specific snippet for a user.
    """
    snippet = db.query(Snippet).filter(
        Snippet.user_str_id == user_str_id,
        Snippet.snippet_name == snippet_name
    ).first()
    
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    
    db.delete(snippet)
    db.commit()
    
    return {"message": f"Snippet '{snippet_name}' deleted successfully"}

@app.get("/users/{user_str_id}/snippets/language/{language}", response_model=List[SnippetSummary])
def get_snippets_by_language(
    user_str_id: str,
    language: str,
    db: Session = Depends(get_db)
):
    """
    Get all snippets for a user filtered by programming language.
    """
    snippets = db.query(Snippet).filter(
        Snippet.user_str_id == user_str_id,
        Snippet.language.ilike(f"%{language}%")
    ).all()
    
    return snippets

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
