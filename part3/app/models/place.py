from app import db
from .base_model import BaseModel

class Place(BaseModel):
    """Class representing a rental place"""
    
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False, default=0.0)
    longitude = db.Column(db.Float, nullable=False, default=0.0)
    
    def __init__(self, title, description="", price=0.0, latitude=0.0, longitude=0.0, **kwargs):
        """Initialize a new Place"""
        super().__init__(**kwargs)
        
        # Validate required fields
        self.validate_title(title)
        
        # Set properties
        self.title = title
        self.description = description
        self.price = price  # Will use the setter with validation
        self.latitude = latitude
        self.longitude = longitude
    
    @staticmethod
    def validate_title(title):
        """Validate place title"""
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
    
    @property
    def price(self):
        """Get price"""
        return self._price
    
    @price.setter
    def price(self, value):
        """Set price with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
    
    @property
    def latitude(self):
        """Get latitude"""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """Set latitude with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if not -90 <= float(value) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        """Get longitude"""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Set longitude with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if not -180 <= float(value) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
    
    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude
        })
        return place_dict
