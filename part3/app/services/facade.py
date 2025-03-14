from uuid import uuid4
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.repository import SQLAlchemyRepository

class Facade:
    def __init__(self):
        """Initialiser les repositories"""
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.review_repository = SQLAlchemyRepository(Review)

    # Méthodes utilisateur
    def get_users(self):
        """Obtenir tous les utilisateurs non-test"""
        users = self.user_repository.get_all()
        # Filtrer les utilisateurs de test
        return [user for user in users if not getattr(user, 'is_test_user', False)]

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        return self.user_repository.add(user)

    def update_user(self, user_id, data):
        return self.user_repository.update(user_id, data)

    # Methods for amenities
    def create_amenity(self, amenity_data):
        """Create a new amenity
        
        Args:
            amenity_data (dict): Amenity data containing name
            
        Returns:
            dict: The created amenity with all attributes
        """
        if not amenity_data.get('name'):
            raise ValueError("Name is required")
        
        amenity = Amenity(name=amenity_data['name'])
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        """Get amenity by ID
        
        Args:
            amenity_id (str): The ID of the amenity to retrieve
                
        Returns:
            Amenity: The amenity if found
                
        Raises:
            ValueError: If the amenity is not found
        """
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Get all amenities
        
        Returns:
            list: List of all amenities
        """
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity
        
        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): New amenity data
        
        Returns:
            Amenity: Updated amenity
        
        Raises:
            ValueError: If amenity not found or data is invalid
        """
        # Validate name is not empty if provided
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
        
        return self.amenity_repository.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        """Create a new place
        
        Args:
            place_data (dict): Data for the place to create
            
        Returns:
            Place: The created place
            
        Raises:
            ValueError: If the data is invalid
        """
        # Title validation (required according to the requirements)
        if not place_data.get('title'):
            raise ValueError("Title is required")
        
        if len(place_data.get('title', '')) > 100:
            raise ValueError("Title must not exceed 100 characters")
            
        # Owner validation - REQUIRED and MUST EXIST
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
            
        # Check if owner exists
        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} does not exist")
        
        # Price validation (positive if specified)
        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")
            
        # Latitude and longitude validation
        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        try:
            # Create place object
            place = Place(
                title=place_data.get('title', 'Untitled'),
                description=place_data.get('description', ''),
                price=float(place_data.get('price', 0.0)),
                latitude=float(place_data.get('latitude', 0.0)),
                longitude=float(place_data.get('longitude', 0.0)),
                owner_id=owner_id
            )
            
            # Handle amenities if provided
            if 'amenities' in place_data:
                amenity_ids = place_data.get('amenities', [])
                for amenity_id in amenity_ids:
                    amenity = self.amenity_repository.get(amenity_id)
                    if amenity:
                        place.amenities.append(amenity)
            
            return self.place_repository.add(place)
            
        except Exception as e:
            print(f"Error in create_place: {str(e)}")
            raise ValueError(f"Failed to create place: {str(e)}")

    def get_place(self, place_id):
        """Get a place by its ID"""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Get all places with full details
        
        Returns:
            list: List of all places with complete information
        """
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        # Check if the place exists
        place = self.place_repository.get(place_id)
        if not place:
            return None
        
        # Validate updated data
        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")
        
        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 et 180")
        
        # Check if owner_id is being updated and if the new owner exists
        if 'owner_id' in place_data:
            owner = self.user_repository.get(place_data['owner_id'])
            if not owner:
                raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")
        
        # Handle amenities if they are updated
        if 'amenities' in place_data:
            # Clear existing amenities and add new ones
            place.amenities = []
            
            amenity_ids = place_data['amenities']
            for amenity_id in amenity_ids:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
            
            # Remove 'amenities' from place_data to avoid SQLAlchemy conflicts
            del place_data['amenities']
        
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place by its ID"""
        return self.place_repository.delete(place_id)

    def create_review(self, review_data):
        """Create a new review
        
        Args:
            review_data (dict): Review data including text, rating, user_id, place_id
                
        Returns:
            Review: The newly created review
            
        Raises:
            ValueError: If the review data is invalid
        """
        # Validate user_id
        user = self.user_repository.get(review_data.get('user_id'))
        if not user:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place_id
        place = self.place_repository.get(review_data.get('place_id'))
        if not place:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Validate rating
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate text
        if not review_data.get('text'):
            raise ValueError("Review text is required")
        
        # Create review object
        review = Review(
            text=review_data.get('text', ''),
            rating=review_data.get('rating', 0),
            user_id=review_data.get('user_id', ''),
            place_id=review_data.get('place_id', '')
        )
        
        return self.review_repository.add(review)

    def get_review(self, review_id):
        """Get review by ID
        
        Args:
            review_id (str): ID of the review to retrieve
            
        Returns:
            Review: The review if found, or None if not found
        """
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Get all reviews
        
        Returns:
            list: List of all reviews
        """
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            list: List of reviews for this place
            
        Raises:
            ValueError: If the place does not exist
        """
        # Validate place exists
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} does not exist")
        
        # Get reviews by place_id attribute
        return self.review_repository.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        """Update an existing review
        
        Args:
            review_id (str): ID of the review to update
            review_data (dict): New review data
            
        Returns:
            Review: The updated review, or None if not found
            
        Raises:
            ValueError: If the data is invalid
        """
        # Check if review exists
        review = self.review_repository.get(review_id)
        if not review:
            return None
        
        # Prevent changing user_id or place_id
        if 'user_id' in review_data and review_data['user_id'] != review.user_id:
            raise ValueError("User ID cannot be changed in a review update")
            
        if 'place_id' in review_data and review_data['place_id'] != review.place_id:
            raise ValueError("Place ID cannot be changed in a review update")
        
        # Validate rating if provided
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate text if provided
        if 'text' in review_data and not review_data['text']:
            raise ValueError("Review text is required")
        
        return self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review
        
        Args:
            review_id (str): ID of the review to delete
            
        Returns:
            bool: True if successfully deleted, False otherwise
        """
        return self.review_repository.delete(review_id)

    def get_places(self):
        """Get all places
        
        Returns:
            list: List of all places
        """
        return self.place_repository.get_all()
