# eCommerce API

A comprehensive Django REST Framework backend for an e-commerce platform providing robust API endpoints for managing products, orders, users, and more.

## 🚀 Features

### Core Modules
- **Accounts** - User authentication, registration, and profile management
- **Products** - Product catalog management with categories and inventory
- **Orders** - Shopping cart functionality and order processing
- **Reviews** - Product reviews and rating system
- **Recommendations** - AI-powered product recommendation engine
- **Notifications** - User notification system
- **Admin Dashboard** - Administrative functionality and analytics

### Key Features
- ✅ RESTful API architecture
- ✅ JWT Authentication
- ✅ User registration and profile management
- ✅ Product catalog with categories
- ✅ Shopping cart and checkout process
- ✅ Order management and tracking
- ✅ Product reviews and ratings
- ✅ AI-based product recommendations
- ✅ Real-time notifications
- ✅ Admin dashboard with analytics
- ✅ API documentation with Swagger/OpenAPI
- ✅ Comprehensive test coverage

## 🛠️ Technology Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Testing**: Django Test Framework
- **Task Queue**: Celery + Redis (for async tasks)
- **Storage**: Django Static Files / AWS S3 (for media)

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8+
- pip (Python package installer)
- PostgreSQL (for production)
- Redis (for caching and task queue)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hasninemamud/eCommerce-API.git
cd eCommerce-API
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory and add the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ecommerce_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=7

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Payment Integration (Optional)
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# AWS S3 (Optional - for media files)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

### 5. Database Setup

```bash
# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication
The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 🔗 API Endpoints

### Authentication Endpoints
```
POST   /api/v1/auth/register/          # User registration
POST   /api/v1/auth/login/             # User login
POST   /api/v1/auth/logout/            # User logout
POST   /api/v1/auth/refresh/           # Refresh JWT token
POST   /api/v1/auth/password/reset/    # Password reset
GET    /api/v1/auth/profile/           # Get user profile
PUT    /api/v1/auth/profile/           # Update user profile
```

### Product Endpoints
```
GET    /api/v1/products/               # List all products
POST   /api/v1/products/               # Create new product (Admin)
GET    /api/v1/products/{id}/          # Get product details
PUT    /api/v1/products/{id}/          # Update product (Admin)
DELETE /api/v1/products/{id}/          # Delete product (Admin)
GET    /api/v1/products/categories/    # List product categories
GET    /api/v1/products/featured/      # Get featured products
GET    /api/v1/products/search/        # Search products
```

### Order Endpoints
```
GET    /api/v1/orders/                 # List user orders
POST   /api/v1/orders/                 # Create new order
GET    /api/v1/orders/{id}/            # Get order details
PUT    /api/v1/orders/{id}/            # Update order status
GET    /api/v1/cart/                   # Get shopping cart
POST   /api/v1/cart/add/               # Add item to cart
PUT    /api/v1/cart/update/            # Update cart item
DELETE /api/v1/cart/remove/            # Remove item from cart
POST   /api/v1/checkout/               # Process checkout
```

### Review Endpoints
```
GET    /api/v1/reviews/                # List reviews
POST   /api/v1/reviews/                # Create review
GET    /api/v1/reviews/{id}/           # Get review details
PUT    /api/v1/reviews/{id}/           # Update review
DELETE /api/v1/reviews/{id}/           # Delete review
GET    /api/v1/products/{id}/reviews/  # Get product reviews
```

### Recommendation Endpoints
```
GET    /api/v1/recommendations/        # Get personalized recommendations
GET    /api/v1/recommendations/trending/ # Get trending products
GET    /api/v1/recommendations/similar/{product_id}/ # Get similar products
```

### Notification Endpoints
```
GET    /api/v1/notifications/          # List user notifications
PUT    /api/v1/notifications/{id}/read/ # Mark notification as read
DELETE /api/v1/notifications/{id}/     # Delete notification
```

### Admin Dashboard Endpoints
```
GET    /api/v1/admin/dashboard/        # Dashboard statistics
GET    /api/v1/admin/users/            # Manage users
GET    /api/v1/admin/orders/           # Manage orders
GET    /api/v1/admin/analytics/        # Analytics data
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


