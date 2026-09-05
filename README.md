# RevoShop API

RevoShop API is a RESTful backend for an online store application built with Flask and PostgreSQL.

The application provides endpoints for managing users, products, categories, orders, and order items. SQLAlchemy is used as the ORM, while Flask-Migrate and Alembic are used to manage database migrations.

---

## Project Overview

RevoShop is a backend API for an online store.

The application provides:

- User registration
- User login
- User management
- Product management
- Category management
- Order management
- Order item management
- Product stock management
- Input validation
- Error handling
- Database migrations
- Automated testing
- Load testing
- Production deployment

The API uses PostgreSQL as its relational database and exposes its functionality through RESTful API endpoints.

---

# Features

## User Management

- Register a new user
- Retrieve all users
- Retrieve a user by ID
- Login using email and password
- Password hashing
- User role support

## Product Management

- Create product
- Retrieve all products
- Retrieve product by ID
- Update product
- Delete product
- Product validation
- Product stock management
- Prevent deletion of products associated with active orders

## Category Management

- Create category
- Retrieve all categories
- Retrieve category by ID
- Update category
- Delete category
- Category validation
- Prevent deletion of categories that still contain products

## Order Management

- Create order
- Retrieve all orders
- Retrieve order by ID
- Update order status
- Delete order
- Associate orders with users
- Associate orders with products through `order_items`
- Automatically decrease product stock when an order is created
- Restore product stock when an order is deleted

## Validation and Error Handling

The API validates incoming data and returns meaningful JSON error responses.

Validation includes:

- Required fields
- Empty values
- Invalid price
- Invalid stock
- Invalid category
- Invalid user
- Invalid order items
- Duplicate category
- Product not found
- Category not found
- Order not found

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Flask | Web framework |
| Flask-SQLAlchemy | Flask database integration |
| SQLAlchemy | ORM |
| Flask-Migrate | Database migration management |
| Alembic | Migration engine |
| PostgreSQL | Relational database |
| psycopg2-binary | PostgreSQL driver |
| python-dotenv | Environment variable management |
| pytest | Automated testing |
| Locust | Load testing |
| Waitress | Local WSGI server |
| pgAdmin | PostgreSQL administration |
| Supabase | Production PostgreSQL hosting |
| Vercel | Production API deployment |

---

# Project Structure

```text
Paramita/
│
├── api/
│   └── index.py
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes.py
│
├── migrations/
│   ├── versions/
│   │   ├── 0001_initial_schema.py
│   │   └── 1cdd4502dff8_add_role_to_users.py
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── test_category.py
│   ├── test_order.py
│   └── test_product.py
│
├── .env.example
├── .gitignore
├── create_tables.py
├── locustfile.py
├── locust.png
├── postman-delete.png
├── postman-get.png
├── postman-post.png
├── postman-put.png
├── pytest.ini
├── pytest.png
├── queries.sql
├── README.md
├── requirements.txt
├── run.py
├── schema.sql
├── seed.sql
├── supabase-order.png
└── supabase-tables.png
```

> The `.env` file is used for local configuration and must not be committed to GitHub.

---

# API Base URL

## Local Development

```text
http://127.0.0.1:5000
```

## Production

```text
https://paramita-tan.vercel.app
```

---

# Health Check

## Endpoint

```http
GET /api
```

Expected response:

```json
{
  "message": "RevoShop API is running",
  "status": "success"
}
```

---

# API Documentation

## User Endpoints

### Register User

```http
POST /users
```

Example request:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

### Get All Users

```http
GET /users
```

### Get User by ID

```http
GET /users/<id>
```

Example:

```http
GET /users/1
```

### Login

```http
POST /auth/login
```

Example request:

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

---

# Product Endpoints

## Create Product

```http
POST /products
```

Example request:

```json
{
  "name": "Laptop",
  "description": "Laptop for work and study",
  "price": 10000000,
  "stock": 10,
  "category_id": 1
}
```

Expected success response:

```text
201 Created
```

## Get All Products

```http
GET /products
```

## Get Product by ID

```http
GET /products/<id>
```

Example:

```http
GET /products/1
```

## Update Product

```http
PUT /products/<id>
```

Example request:

```json
{
  "name": "Laptop Updated",
  "price": 12000000,
  "stock": 8
}
```

## Delete Product

```http
DELETE /products/<id>
```

A product associated with an active order cannot be deleted.

---

# Category Endpoints

## Create Category

```http
POST /categories
```

Example request:

```json
{
  "name": "Electronics"
}
```

## Get All Categories

```http
GET /categories
```

## Get Category by ID

```http
GET /categories/<id>
```

## Update Category

```http
PUT /categories/<id>
```

Example request:

```json
{
  "name": "Electronic Devices"
}
```

## Delete Category

```http
DELETE /categories/<id>
```

A category containing products cannot be deleted.

---

# Order Endpoints

## Create Order

```http
POST /orders
```

Example request:

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

When an order is successfully created:

- The order is associated with a user.
- Order items are associated with products.
- Product stock is decreased automatically.

## Get All Orders

```http
GET /orders
```

Optional user filter:

```http
GET /orders?user_id=1
```

## Get Order by ID

```http
GET /orders/<id>
```

Example:

```http
GET /orders/1
```

## Update Order

```http
PUT /orders/<id>
```

Example request:

```json
{
  "status": "completed"
}
```

## Delete Order

```http
DELETE /orders/<id>
```

When an order is deleted, related product stock is restored.

---

# Database Schema

The RevoShop PostgreSQL database contains five main tables:

```text
users
products
categories
orders
order_items
```

## Users

```text
users
--------------------------------
id
name
email
password
created_at
role
```

The `email` field is unique.

## Categories

```text
categories
--------------------------------
id
name
```

The `name` field is unique.

## Products

```text
products
--------------------------------
id
name
description
price
stock
category_id
```

Relationship:

```text
products.category_id
        |
        v
categories.id
```

## Orders

```text
orders
--------------------------------
id
user_id
total
status
created_at
```

Relationship:

```text
orders.user_id
        |
        v
users.id
```

## Order Items

```text
order_items
--------------------------------
id
order_id
product_id
quantity
price
```

Relationships:

```text
order_items.order_id
        |
        v
orders.id

order_items.product_id
        |
        v
products.id
```

---

# Database Relationship

```text
Users
  |
  | 1
  |
  └──────────────< Orders
                    |
                    | 1
                    |
                    └──────────────< Order Items >────────────── Products
                                                                    |
                                                                    |
                                                                    └──── Categories
```

The `order_items` table connects orders and products while storing the quantity and price of each ordered product.

---

# Database Migration

The project uses Flask-Migrate and Alembic.

## Apply migrations

```bash
flask db upgrade
```

## View migration history

```bash
flask db history
```

## Check current migration

```bash
flask db current
```

## Create a new migration

```bash
flask db migrate -m "description of changes"
```

Then apply it:

```bash
flask db upgrade
```

---

# Environment Configuration

Sensitive configuration is stored in environment variables.

Create a `.env` file locally using `.env.example` as a reference.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/revoshop
FLASK_DEBUG=1
```

The `.env` file must not be committed to GitHub.

The repository contains `.env.example` with placeholder values.

---

# Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/nixcenat-stack/Paramita.git
cd Paramita
```

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

## 3. Activate the Virtual Environment

```powershell
venv\Scripts\activate
```

If PowerShell execution policy prevents activation, use:

```powershell
.\venv\Scripts\python.exe
```

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create `.env` based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/revoshop
FLASK_DEBUG=1
```

## 6. Apply Database Migrations

```powershell
flask db upgrade
```

## 7. Run the Application

```powershell
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

# Automated Testing

The project uses pytest for automated API testing.

## Run All Tests

```powershell
pytest -v
```

Or:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Latest automated test result:

```text
48 passed, 102 warnings
```

The warnings did not cause test failures.

![Pytest Result](./pytest.png)

---

# Category Testing

Category tests cover:

- GET all categories
- GET category by ID
- POST category
- PUT category
- DELETE category
- Missing data
- Invalid data
- Duplicate category
- Not found cases
- Deletion restrictions

Run category tests:

```powershell
pytest -v tests/test_category.py
```

---

# Product and Order Testing

Run Product and Order tests:

```powershell
pytest -v tests/test_product.py tests/test_order.py
```

---

# Load Testing with Locust

Locust is used to simulate users interacting with the RevoShop API.

The configured sequential user journey is:

```text
1. GET /products
2. GET /products/<id>
3. POST /orders
4. GET /orders/<id>
```

The load test uses:

```text
Product ID: 66
User ID: 2
```

The Locust configuration is stored in:

```text
locustfile.py
```

## Start the local WSGI server

```powershell
.\venv\Scripts\waitress-serve.exe --listen=127.0.0.1:5000 run:app
```

## Run 50 users

```powershell
.\venv\Scripts\python.exe -m locust --headless -u 50 -r 5 -t 30s --host http://127.0.0.1:5000
```

## Run 200 users

```powershell
.\venv\Scripts\python.exe -m locust --headless -u 200 -r 10 -t 1m --host http://127.0.0.1:5000
```

Where:

```text
-u = number of users
-r = spawn rate
-t = test duration
```

Locust evidence:

![Locust Result](./locust.png)

---

# Production Deployment

The production backend is deployed using Vercel.

## Production API

```text
https://paramita-tan.vercel.app
```

## Production Health Check

```text
https://paramita-tan.vercel.app/api
```

Expected response:

```json
{
  "message": "RevoShop API is running",
  "status": "success"
}
```

## Production Products

```text
https://paramita-tan.vercel.app/products
```

The production API has been tested and verified to return JSON responses.

---

# Production Database

The production PostgreSQL database is hosted on Supabase.

Production project:

```text
revoshop-production
```

Production tables:

```text
users
products
categories
orders
order_items
```

Migrations are applied using:

```bash
flask db upgrade
```

Production database evidence:

![Supabase Tables](./supabase-tables.png)

---

# Order Items Evidence

The production `order_items` table contains:

```text
id
order_id
product_id
quantity
price
```

![Supabase Order Items](./supabase-order.png)

---

# Production API Testing

Production Product CRUD was tested using Postman.

## POST Product

```http
POST /products
```

![Postman POST](./postman-post.png)

## GET Product

```http
GET /products/<id>
```

![Postman GET](./postman-get.png)

## PUT Product

```http
PUT /products/<id>
```

![Postman PUT](./postman-put.png)

## DELETE Product

```http
DELETE /products/<id>
```

![Postman DELETE](./postman-delete.png)

The Product CRUD workflow was tested using:

```text
https://paramita-tan.vercel.app
```

---

# Security

The project uses environment variables to protect sensitive configuration.

Security practices include:

- `.env` is excluded from Git
- `.env.example` contains placeholder values
- Database credentials are not intended to be committed
- Passwords are hashed before storage
- Environment variables are loaded using `python-dotenv`
- Configuration values are accessed through environment variables

---

# GitHub Repository

Repository:

```text
https://github.com/nixcenat-stack/Paramita
```

The repository contains:

- Flask application
- SQLAlchemy models
- API routes
- Database migrations
- Automated tests
- Locust configuration
- PostgreSQL schema
- Sample data
- Environment template
- Documentation
- Testing evidence

---

# Database SQL Files

## schema.sql

Contains SQL statements for creating the database tables.

## seed.sql

Contains sample data for:

- Users
- Categories
- Products
- Orders
- Order Items

## queries.sql

Contains example SQL queries demonstrating:

- `WHERE`
- `ORDER BY`
- `LIMIT`
- JOIN operations
- Order and product relationships

---

# Requirements

Main dependencies:

```text
Flask==3.1.3
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.12
python-dotenv==1.0.1
```

Testing tools:

```text
pytest
Locust
```

---

# Useful Commands

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Apply Migration

```powershell
flask db upgrade
```

## Check Migration History

```powershell
flask db history
```

## Run Tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Run Application

```powershell
python run.py
```

## Start Waitress

```powershell
.\venv\Scripts\waitress-serve.exe --listen=127.0.0.1:5000 run:app
```

## Run Locust

```powershell
.\venv\Scripts\python.exe -m locust --headless -u 50 -r 5 -t 30s --host http://127.0.0.1:5000
```

---

# Project Status

The current RevoShop implementation includes:

- PostgreSQL database
- SQLAlchemy ORM
- Flask REST API
- Flask-Migrate
- User registration
- User login
- User retrieval
- Product CRUD
- Category CRUD
- Order CRUD
- Order items
- Product stock management
- Input validation
- Error handling
- Automated testing with pytest
- Locust load testing configuration
- Supabase production database
- Vercel deployment
- Postman production API testing

Latest automated test result:

```text
48 passed
102 warnings
```

---

# Submission Checklist

- [x] PostgreSQL database configured
- [x] Required database tables created
- [x] Primary keys configured
- [x] Foreign keys configured
- [x] Database migrations created
- [x] Database migrations applied
- [x] User registration implemented
- [x] User login implemented
- [x] User retrieval implemented
- [x] Product CRUD implemented
- [x] Category CRUD implemented
- [x] Order CRUD implemented
- [x] Input validation implemented
- [x] Error handling implemented
- [x] Product deletion guard implemented
- [x] `.env.example` provided
- [x] `.env` excluded with `.gitignore`
- [x] Automated tests implemented
- [x] 48 automated tests passed
- [x] Locust journey configured
- [x] Production PostgreSQL deployed
- [x] Production API deployed
- [x] Product CRUD tested in production with Postman
- [x] GitHub repository available
- [x] README documentation completed
- [x] Pytest evidence uploaded
- [x] Locust evidence uploaded
- [x] Postman evidence uploaded
- [x] Supabase database evidence uploaded
- [x] Order items evidence uploaded

---

# Final Links

## GitHub Repository

https://github.com/nixcenat-stack/Paramita

## Production API

https://paramita-tan.vercel.app

## API Health Check

https://paramita-tan.vercel.app/api

## Production Database

```text
Supabase
Project: revoshop-production
```

---

# RevoShop API

A Flask and PostgreSQL REST API project combining database design, SQLAlchemy ORM, migrations, CRUD operations, automated testing, load testing, and cloud deployment.
