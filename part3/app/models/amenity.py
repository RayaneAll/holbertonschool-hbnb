from app import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey

# Association table for the many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', db.Model.metadata,
    db.Column('place_id', db.String(36), ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    """Class representing an amenity"""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    # Relationships
    places = relationship('Place', secondary=place_amenity, backref='amenities', lazy='subquery')

    def __init__(self, name: str, **kwargs):
        """
        Initialize a new amenity
        Args:
            name (str): Name of the amenity
        """
        super().__init__(**kwargs)
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name: str):
        """Validate amenity name"""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def to_dict(self):
        """Convert amenity to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
