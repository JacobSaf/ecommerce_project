Django eCommerce Platform
A full‑featured eCommerce application built with Django and Django REST Framework, supporting buyers, sellers, stores, products, carts, orders, reviews, and guest checkout.
This project is designed to be easy to run, easy to understand, and easy to extend — perfect for learning, portfolio use, or real‑world adaptation.


 User Accounts
- Custom user model (CustomUser)
- Buyer and seller roles
- Registration with role selection
- Login / logout
- Seller dashboard (stores + products)

Stores
- Sellers can create stores
- Each store can list multiple products

 Products
- Product CRUD for sellers
- Categories
- Stock tracking
- Product images
- SKU system
- Product detail pages

 Shopping Cart
- Logged‑in users: database‑backed cart
- Guests: session‑based cart
- Add, update, remove items
- Automatic total calculation

 Checkout
- Logged‑in checkout
- Guest checkout with form
- Stock validation
- Order + OrderItem creation
- Email invoice sending

Reviews
- Users can leave reviews
- Verified purchase detection
- API endpoint for product reviews

 REST API
- Product API
- Store API
- Review API

Project Structure. 
ecommerce/
│
├── accounts/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── products/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── stores/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── orders/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── reviews/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
└── ecommerce/ (project root)
    ├── settings.py
    ├── urls.py
    └── wsgi.py

Getting Started:
1. Clone the repository
git clone <your-repo-url>
cd ecommerce

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3.Install Dependencies
pip install -r requirements.txt

4. Apply Migrations
python manage.py migrate

5. Create a Superuser
python manage.py createsuperuser

6. Run the Development Server
python manage.py runserver

7. Visit the site at:
http://127.0.0.1:8000/

Running with Docker
1. Build the Docker image:
docker build -t ecommerce_project

2. Run the container:
docker run -p 8000:8000 ecommerce_project

Running with Docker Compose
1. Ensure Docker and Docker Compose are installed.
2. Start containers
docker-compose up --build
3. Apply migrations
docker-compose exec web python manage.py migrate
4. Create a superuser:
docker-compose exec web python manage.py createsuperuser
5. Access the app:
http://localhost:8000

Security Notes
-Do NOT commit secrets (passwords, tokens) to GitHub.
-Use a .env file for sensitive values.
-Add .env to .gitignore


Testing the Project
-Register as a buyer or seller
-Login/logout
-Access seller dashboard if is_seller=True

Stores
-Sellers can create stores
-Stores can contain multiple projects

Products
-Add/Edit/Delete products
-Upload images
-Assign Categories

Cart
-Add items from product pages
-Update quantities
-Remove items
-Works for both logged-in and guest users

Checkout
-Logged-in checkout uses user email
-Guest checkout collects shipping info
-Stock is validated before purchase
-Order + OrderItems created
-Email invoice sent

Reviews
-Leave reviews on product pages
-Verified purchase detection
API endpoint: /api/products/<id>/reviews/

API Endpoints
Products:
GET /api/products/
GET /api/products/<id>/

Stores:
GET /api/stores/
GET /api/stores/<id>/

Reviews
GET /api/products/<product_id>/reviews/

Email Sending
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"