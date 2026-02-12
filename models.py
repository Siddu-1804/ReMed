from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Registration(Base):
    """User registration model"""
    __tablename__ = "registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    phone_number = Column(String(20), index=True, nullable=False)
    registration_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Confirmed")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "phoneNumber": self.phone_number,
            "registrationTime": self.registration_time.isoformat() if self.registration_time else None,
            "status": self.status
        }
