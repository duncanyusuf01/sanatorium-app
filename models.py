from app import db  # Import the db instance from app.py
from datetime import datetime

class Product(db.Model):
    """
    Model for products sold in the boutique.
    """
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'flowers', 'clothes', 'art', 'accessories'
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Service(db.Model):
    """
    Model for bookable services.
    """
    __tablename__ = 'service'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

class Booking(db.Model):
    """
    Model for booking requests from users.
    """
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))
    
    plan_type = db.Column(db.String(50), nullable=False)  # 'hourly', 'halfday', 'fullday', etc.
    requested_date = db.Column(db.Date, nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False) # 'pending', 'confirmed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id} by {self.full_name}>'
