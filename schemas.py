from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RegistrationCreate(BaseModel):
    """Schema for creating a registration"""
    name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=5, max_length=20)

class RegistrationResponse(BaseModel):
    """Schema for registration response"""
    id: int
    name: str
    phoneNumber: str

    
    class Config:
        from_attributes = True

class RegistrationSubmit(BaseModel):
    """Schema for form submission - simplified"""
    name: str
    phoneNumber: str
