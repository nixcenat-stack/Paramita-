# RevoShop API

RevoShop API is a RESTful backend for an online store application.

The project provides API endpoints for managing users, products, categories, orders, and order items. The application is built with Flask, SQLAlchemy, Flask-Migrate, and PostgreSQL.

---

## Project Overview

RevoShop is a backend API designed to support the core functionality of an online store.

The system provides:

- User registration and login
- User management
- Product management
- Category management
- Order management
- Order item management
- Product stock management
- Input validation
- Error handling
- Database migrations
- Automated API testing
- Load testing
- Production deployment

The application uses PostgreSQL as the relational database and exposes functionality through a RESTful API.

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

- Create a product
- Retrieve all products
- Retrieve a product by ID
- Update a product
- Delete a product
- Validate product input
- Manage product stock
- Prevent deletion of products linked to active orders

## Category Management

- Create a category
- Retrieve all categories
- Retrieve a category by ID
- Update a category
- Delete a category
- Validate category input
- Prevent deletion of categories that still contain products

## Order Management

- Create an order
- Retrieve all orders
- Retrieve an order by ID
- Update order status
- Delete an order
- Associate orders with users
- Associate orders with products through `order_items`
- Automatically decrease product stock when an order is created
- Restore product stock when an order is deleted

## Validation and Error Handling

The API validates user input and returns meaningful error responses for invalid requests.

Examples include:

- Missing required fields
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
| Flask-SQLAlchemy | SQLAlchemy integration for Flask |
| SQLAlchemy | Object-relational mapping |
| Flask-Migrate | Database migration management |
| Alembic | Migration engine |
| PostgreSQL | Relational database |
| psycopg2-binary | PostgreSQL database driver |
| python-dotenv | Environment variable management |
| pytest | Automated testing |
| Locust | Load testing |
| pgAdmin | PostgreSQL administration |
| Supabase | Production PostgreSQL hosting |
| Vercel | Production API deployment |
| Waitress | Local WSGI server for load testing |

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
├── pytest.ini
├── queries.sql
├── README.md
├── requirements.txt
├── run.py
├── schema.sql
└── seed.sql
---

# Testing & Evidence

## Automated Testing

The project was tested using pytest.

Latest result:

```text
48 passed, 102 warnings
