from app import db
from .base_model import BaseModel

class Amenity(BaseModel):
    """Class representing an amenity"""
    
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False)
    
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
