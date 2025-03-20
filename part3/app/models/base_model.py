from uuid import uuid4
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base class for all models using SQLAlchemy"""
    __abstract__ = True  # Ensure SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save or update the instance in the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Return dictionary representation of the instance"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
