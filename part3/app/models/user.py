from .base_model import BaseModel
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    """Represents a user in the system.

    This class manages user information including identification,
    personal details, contact information, and authentication.

    Attributes:
        id (str): Unique identifier for the user
        first_name (str): User's first name, max 50 characters
        last_name (str): User's last name, max 50 characters
        email (str): User's email address
        password (str): Hashed password for authentication
        is_admin (bool): Admin status, defaults to False
        created_at (DateTime): Timestamp when the user is created
        updated_at (DateTime): Timestamp when the user is last updated
    """
    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        """Initialize a new User instance.

        Args:
            first_name (str): User's first name
            last_name (str): User's last name 
            email (str): User's email address
            password (str): User's raw password (to be hashed)
            is_admin (bool, optional): Admin status. Defaults to False.
        """
        super().__init__(**kwargs)

        # Explicit validation with clear error messages
        if not first_name or first_name.strip() == "":
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less")

        if not last_name or last_name.strip() == "":
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")

        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")

        # Email format validation
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.reviews = []  # List of reviews by this user
        self.password = None  # Placeholder for hashed password

        self.hash_password(password)  # Hash the password during initialization

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user instance to dictionary representation without exposing the password."""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict  # Excluding the password for security reasons
