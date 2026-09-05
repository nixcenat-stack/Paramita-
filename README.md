# RevoShop API

RevoShop API is a RESTful backend for an online store application built with Flask and PostgreSQL.

The API manages users, products, categories, orders, and order items through a RESTful interface. The project uses SQLAlchemy as the ORM and Flask-Migrate with Alembic for database migrations.

---

## Project Overview

RevoShop provides the backend functionality required for an online store, including:

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

The application uses PostgreSQL as the relational database and exposes its functionality through REST API endpoints.

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
- Retrieve a product by ID
- Update product
- Delete product
- Product input validation
- Product stock management
- Prevent deletion of products associated with active orders

## Category Management

- Create category
- Retrieve all categories
- Retrieve a category by ID
- Update category
- Delete category
- Category input validation
- Prevent deletion of categories that still contain products

## Order Management

- Create order
- Retrieve all orders
- Retrieve an order by ID
- Update order status
- Delete order
- Associate orders with users
- Associate orders with products through `order_items`
- Automatically decrease product stock when an order is created
- Restore product stock when an order is deleted

## Validation and Error Handling

The API validates incoming data and returns meaningful JSON responses.

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
| Vercel | Production deployment |

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
