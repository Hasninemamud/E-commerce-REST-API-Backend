# E-commerce API

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen.svg)]()

A comprehensive, production-ready Django REST Framework backend for modern e-commerce platforms. Built with scalability, security, and developer experience in mind.

## 🎯 Overview

This API provides a complete backend solution for e-commerce applications, featuring user management, product catalogs, order processing, payment integration, and AI-powered recommendations. Perfect for building web applications, mobile apps, or headless commerce solutions.

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication with refresh tokens
- User registration and profile management
- Password reset and email verification
- Role-based access control (RBAC)
- Rate limiting and security headers

### 📦 Product Management
- Comprehensive product catalog
- Category and subcategory organization
- Inventory tracking and stock management
- Product search and filtering
- Image and media file handling

### 🛒 Order Processing
- Shopping cart functionality
- Secure checkout process
- Order tracking and status updates
- Payment gateway integration
- Invoice generation

### ⭐ Reviews & Ratings
- Product review system
- Star rating aggregation
- Review moderation
- User feedback analytics

### 🤖 AI-Powered Features
- Personalized product recommendations
- Trending products analysis
- Similar product suggestions
- Customer behavior insights

### 📬 Communication
- Real-time notification system
- Email notifications
- Order status updates
- Marketing campaign support

### 📊 Analytics & Admin
- Comprehensive admin dashboard
- Sales analytics and reporting
- User behavior tracking
- Inventory management tools

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App    │    │   Third-party   │
│   (React/Vue)   │    │   (iOS/Android) │    │   Integrations  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴──────────────┐
                    │       API Gateway          │
                    │    (Load Balancer)         │
                    └─────────────┬──────────────┘
                                 │
                    ┌─────────────┴──────────────┐
                    │    Django REST API         │
                    │  ┌─────────────────────┐   │
                    │  │   Authentication    │   │
                    │  │   Products          │   │
                    │  │   Orders            │   │
                    │  │   Reviews           │   │
                    │  │   Recommendations   │   │
                    │  │   Notifications     │   │
                    │  │   Admin Dashboard   │   │
                    │  └─────────────────────┘   │
                    └─────────────┬──────────────┘
                                  │
                                  |
                                  │                      
                        ┌─────────┴───────┐    
                        │    PostgreSQL   │   
                        │    (Database)   │    
                        └─────────────────┘    
```

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **PostgreSQL 12+**
- **Redis 6+**
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hasninemamud/eCommerce-API.git
   cd eCommerce-API
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

🎉 **Your API is now running at** `http://localhost:8000/`

## 📖 API Documentation

### Interactive Documentation
- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **ReDoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- **OpenAPI Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication
All protected endpoints require JWT authentication:
```http
Authorization: Bearer <your-jwt-token>
```

### Core Endpoints

<details>
<summary><strong>🔐 Authentication</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register/` | User registration |
| `POST` | `/auth/login/` | User login |
| `POST` | `/auth/logout/` | User logout |
| `POST` | `/auth/refresh/` | Refresh JWT token |
| `POST` | `/auth/password/reset/` | Password reset |
| `GET` | `/auth/profile/` | Get user profile |
| `PUT` | `/auth/profile/` | Update user profile |

</details>

<details>
<summary><strong>📦 Products</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products/` | List all products |
| `POST` | `/products/` | Create product (Admin) |
| `GET` | `/products/{id}/` | Get product details |
| `PUT` | `/products/{id}/` | Update product (Admin) |
| `DELETE` | `/products/{id}/` | Delete product (Admin) |
| `GET` | `/products/categories/` | List categories |
| `GET` | `/products/featured/` | Featured products |
| `GET` | `/products/search/` | Search products |

</details>

<details>
<summary><strong>🛒 Orders & Cart</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders/` | List user orders |
| `POST` | `/orders/` | Create new order |
| `GET` | `/orders/{id}/` | Get order details |
| `PUT` | `/orders/{id}/` | Update order status |
| `GET` | `/cart/` | Get shopping cart |
| `POST` | `/cart/add/` | Add item to cart |
| `PUT` | `/cart/update/` | Update cart item |
| `DELETE` | `/cart/remove/` | Remove from cart |
| `POST` | `/checkout/` | Process checkout |

</details>

<details>
<summary><strong>⭐ Reviews</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/reviews/` | List reviews |
| `POST` | `/reviews/` | Create review |
| `GET` | `/reviews/{id}/` | Get review details |
| `PUT` | `/reviews/{id}/` | Update review |
| `DELETE` | `/reviews/{id}/` | Delete review |
| `GET` | `/products/{id}/reviews/` | Product reviews |

</details>

<details>
<summary><strong>🤖 Recommendations</strong></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/recommendations/` | Personalized recommendations |
| `GET` | `/recommendations/trending/` | Trending products |
| `GET` | `/recommendations/similar/{id}/` | Similar products |

</details>

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_NAME=ecommerce_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=7

# Redis
REDIS_URL=redis://localhost:6379/0

# Payment Gateway
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

## 🚀 Deployment

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```


- **Error Tracking**: Sentry integration for error monitoring

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Run tests**
   ```bash
   python manage.py test
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Code of Conduct
Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.


## 📈 Roadmap

- [ ] GraphQL API support
- [ ] Real-time WebSocket notifications
- [ ] Multi-vendor marketplace features
- [ ] Advanced analytics dashboard
- [ ] Mobile SDK development
- [ ] Kubernetes deployment manifests

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

[Report Bug](https://github.com/Hasninemamud/eCommerce-API/issues) • [Request Feature](https://github.com/Hasninemamud/eCommerce-API/issues) • [Documentation](https://github.com/Hasninemamud/eCommerce-API/wiki)

</div>
