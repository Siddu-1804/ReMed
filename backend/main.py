from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from database import engine, get_db
from models import Registration
from schemas import RegistrationSubmit, RegistrationResponse
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReMed API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JavaScript, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    """Serve the main landing page"""
    return FileResponse("templates/index.html", media_type="text/html")

@app.post("/api/register", response_model=RegistrationResponse)
def register_user(registration: RegistrationSubmit, db: Session = Depends(get_db)):
    """
    Register a new user with name and phone number.
    Stores data in SQLAlchemy database.
    """
    # Check if phone number already exists
    existing_user = db.query(Registration).filter(
        Registration.phone_number == registration.phoneNumber
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    # Create new registration record
    new_registration = Registration(
        name=registration.name,
        phone_number=registration.phoneNumber,
        status="Confirmed"
    )
    
    # Save to database
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    
    return new_registration

@app.get("/api/registrations", response_model=list[RegistrationResponse])
def get_registrations(db: Session = Depends(get_db)):
    """
    Get all registrations from the database.
    """
    registrations = db.query(Registration).all()
    return registrations

@app.get("/api/registrations/{registration_id}", response_model=RegistrationResponse)
def get_registration(registration_id: int, db: Session = Depends(get_db)):
    """
    Get a specific registration by ID.
    """
    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    return registration

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "ReMed API"}


#hello 