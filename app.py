import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Database Initialization ---
db = SQLAlchemy(app)

# Import models *after* db is initialized to avoid circular imports
from models import Product, Service, Booking
@app.context_processor
def inject_current_year():
    """Injects the current year into all templates."""
    return {'current_year': datetime.now().year}

# --- Routes ---

@app.route('/')
def index():
    """Homepage: Shows hero, previews of products and services."""
    # Get 6 products for the homepage preview
    products = Product.query.limit(6).all()
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    """About Us page."""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page: Lists all available services from the database."""
    services = Service.query.order_by(Service.id).all()
    return render_template('services.html', services=services)

@app.route('/products')
def products():
    """Products (Boutique) page: Shows a filterable gallery of all products."""
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """
    Booking page:
    GET: Displays the booking form, populated with services.
    POST: Processes the form, validates, and saves a new Booking to the DB.
    """
    if request.method == 'POST':
        try:
            # --- Form Data Retrieval ---
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            service_id = request.form.get('service_id')
            plan_type = request.form.get('plan_type')
            requested_date_str = request.form.get('requested_date')
            message = request.form.get('message')

            # --- Basic Validation ---
            if not all([full_name, email, phone_number, service_id, plan_type, requested_date_str]):
                flash('Please fill out all required fields.', 'error')
                # Need to re-populate services for the template on failure
                services = Service.query.order_by(Service.name).all()
                return render_template('booking.html', services=services), 400

            # --- Data Conversion & Sanitization ---
            try:
                requested_date = datetime.strptime(requested_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
                services = Service.query.order_by(Service.name).all()
                return render_template('booking.html', services=services), 400
            
            # --- Create New Booking ---
            new_booking = Booking(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                service_id=int(service_id),
                plan_type=plan_type,
                requested_date=requested_date,
                message=message,
                status='pending'
            )
            
            db.session.add(new_booking)
            db.session.commit()

            flash('Your booking request has been sent! We will contact you soon.', 'success')
            return redirect(url_for('booking'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error processing booking: {str(e)}")
            flash(f'An error occurred while submitting your request. Please try again.', 'error')

    # --- GET Request Handling ---
    # Fetch services to populate the dropdown
    services = Service.query.order_by(Service.name).all()
    return render_template('booking.html', services=services)

@app.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

# --- CLI Database Commands ---

@app.cli.command('init_db')
def init_db_command():
    """Creates the database tables."""
    try:
        db.create_all()
        print('Initialized the database.')
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.cli.command('seed_db')
def seed_db_command():
    """Seeds the database with sample data for testing."""
    
    # Clear existing data
    print("Deleting old data...")
    db.session.query(Booking).delete()
    db.session.query(Product).delete()
    db.session.query(Service).delete()
    db.session.commit()

    try:
        # --- Add Services ---
        print("Seeding services...")
        s1 = Service(name="Event Space - Studio A", description="Our 100sqm flagship studio, perfect for large workshops, pop-ups, and events.", base_price=100.00)
        s2 = Service(name="Event Space - Studio B", description="An intimate, 50sqm naturally-lit space for photoshoots or small gatherings.", base_price=75.00)
        s3 = Service(name="Co-Working Desk", description="A dedicated hot-desk in our creative co-working zone. Includes Wi-Fi and coffee.", base_price=15.00)
        s4 = Service(name="Subletting Shelf", description="Display your brand's products in our curated boutique. Price is per-week.", base_price=50.00)
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        # --- Add Products ---
        print("Seeding products...")
        p1 = Product(name="Hand-Tied Bouquet", description="Fresh, local flowers arranged daily.", price=45.00, category="flowers", image_url="/static/images/placeholder.jpg")
        p2 = Product(name="Linen Tunic", description="Locally made 100% linen garment.", price=120.00, category="clothes", image_url="/static/images/placeholder.jpg")
        p3 = Product(name="Abstract Canvas", description="Original 24x36 art by a Nairobi local.", price=300.00, category="art", image_url="/static/images/placeholder.jpg")
        p4 = Product(name="Beaded Earrings", description="Handcrafted Maasai beaded accessories.", price=25.00, category="accessories", image_url="/static/images/placeholder.jpg")
        p5 = Product(name="Ceramic Vase", description="Minimalist artisan pottery for your home.", price=60.00, category="art", image_url="/static/images/placeholder.jpg")
        p6 = Product(name="Designer Shirt", description="From the latest collection of a local designer.", price=85.00, category="clothes", image_url="/static/images/placeholder.jpg")
        p7 = Product(name="Dried Flower Bundle", description="A long-lasting dried arrangement.", price=30.00, category="flowers", image_url="/static/images/placeholder.jpg")
        p8 = Product(name="Brass Cuff", description="A statement brass accessory, hand-hammered.", price=55.00, category="accessories", image_url="/static/images/placeholder.jpg")
        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        db.session.commit()
        
        print("Database seeded with sample data.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")


# --- Run Application ---
if __name__ == '__main__':
    # Ensure the static/images directory exists
    os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)
    app.run(debug=True)