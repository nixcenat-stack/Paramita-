from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, Category, Product, Order, OrderItem


main = Blueprint("main", __name__)


# ============================================================
# API
# ============================================================

@main.route("/api", methods=["GET"])
def api():
    return jsonify({
        "message": "RevoShop API is running",
        "status": "success"
    }), 200


# ============================================================
# PRODUCTS
# ============================================================

@main.route("/products", methods=["GET"])
def products():
    products_list = Product.query.all()

    return jsonify([
        product.to_dict()
        for product in products_list
    ]), 200


@main.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


@main.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    category_id = data.get("category_id")

    if name is None:
        return jsonify({
            "message": "name is required"
        }), 400

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    if price is None:
        return jsonify({
            "message": "Price is required"
        }), 400

    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({
            "message": "Price must be a non-negative number"
        }), 400

    if stock is None:
        return jsonify({
            "message": "Stock is required"
        }), 400

    if not isinstance(stock, int) or stock < 0:
        return jsonify({
            "message": "Stock must be a non-negative integer"
        }), 400

    if category_id is None:
        return jsonify({
            "message": "Category ID is required"
        }), 400

    category = Category.query.get(category_id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    try:
        product = Product(
            name=name.strip(),
            description=description,
            price=price,
            stock=stock,
            category_id=category_id
        )

        db.session.add(product)
        db.session.commit()

        return jsonify(product.to_dict()), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "message": "Failed to create product"
        }), 400

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "name" in data:
        name = data.get("name")

        if name is None:
            return jsonify({
                "message": "name is required"
            }), 400

        if not isinstance(name, str) or not name.strip():
            return jsonify({
                "message": "Name must be a non-empty string"
            }), 400

        product.name = name.strip()

    if "description" in data:
        product.description = data.get("description")

    if "price" in data:
        price = data.get("price")

        if not isinstance(price, (int, float)) or price < 0:
            return jsonify({
                "message": "Price must be a non-negative number"
            }), 400

        product.price = price

    if "stock" in data:
        stock = data.get("stock")

        if not isinstance(stock, int) or stock < 0:
            return jsonify({
                "message": "Stock must be a non-negative integer"
            }), 400

        product.stock = stock

    if "category_id" in data:
        category_id = data.get("category_id")

        if category_id is None:
            return jsonify({
                "message": "Category ID is required"
            }), 400

        category = Category.query.get(category_id)

        if not category:
            return jsonify({
                "message": "Category not found"
            }), 404

        product.category_id = category_id

    try:
        db.session.commit()

        return jsonify(product.to_dict()), 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "message": "Failed to update product"
        }), 400

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    if product.order_items:
        return jsonify({
            "message": "Cannot delete product because it is linked to an order"
        }), 409

    try:
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Product deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


# ============================================================
# CATEGORIES
# ============================================================

@main.route("/categories", methods=["GET"])
def categories():
    categories_list = Category.query.all()

    return jsonify([
        {
            "id": category.id,
            "name": category.name
        }
        for category in categories_list
    ]), 200


@main.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "id": category.id,
        "name": category.name,
        "products": [
            product.to_dict()
            for product in category.products
        ]
    }), 200


@main.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")

    if name is None:
        return jsonify({
            "message": "name is required"
        }), 400

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    existing_category = Category.query.filter_by(
        name=name.strip()
    ).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 409

    try:
        category = Category(
            name=name.strip()
        )

        db.session.add(category)
        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name
        }), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "message": "Category already exists"
        }), 409

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")

    if name is None:
        return jsonify({
            "message": "name is required"
        }), 400

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    existing_category = Category.query.filter(
        Category.name == name.strip(),
        Category.id != id
    ).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 409

    try:
        category.name = name.strip()

        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name
        }), 200

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "message": "Category already exists"
        }), 409

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    if category.products:
        return jsonify({
            "message": "Category cannot be deleted because it has products"
        }), 409

    try:
        db.session.delete(category)
        db.session.commit()

        return jsonify({
            "message": "Category deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


# ============================================================
# USERS
# ============================================================

@main.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "message": "Name must be a non-empty string"
        }), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "message": "Email is required"
        }), 400

    if not isinstance(password, str) or len(password) < 6:
        return jsonify({
            "message": "Password must be at least 6 characters"
        }), 400

    existing_user = User.query.filter_by(
        email=email.strip()
    ).first()

    if existing_user:
        return jsonify({
            "message": "Email already registered"
        }), 409

    try:
        user = User(
            name=name.strip(),
            email=email.strip(),
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }), 201

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "message": "Email already registered"
        }), 409

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/users", methods=["GET"])
def users():
    users_list = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }
        for user in users_list
    ]), 200


@main.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at.isoformat()
    }), 200


# ============================================================
# AUTH
# ============================================================

@main.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(
        email=email.strip()
    ).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200


# ============================================================
# ORDERS
# ============================================================

@main.route("/orders", methods=["GET"])
def orders():
    user_id = request.args.get("user_id", type=int)

    query = Order.query

    if user_id is not None:
        query = query.filter_by(user_id=user_id)

    orders_list = query.all()

    return jsonify([
        {
            "id": order.id,
            "user_id": order.user_id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order.order_items
            ]
        }
        for order in orders_list
    ]), 200


@main.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "total": float(order.total),
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price),
                "product": {
                    "id": item.product.id,
                    "name": item.product.name,
                    "description": item.product.description,
                    "price": float(item.product.price),
                    "stock": item.product.stock,
                    "category_id": item.product.category_id
                } if item.product else None
            }
            for item in order.order_items
        ]
    }), 200


@main.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    user_id = data.get("user_id")
    items = data.get("items")

    if user_id is None:
        return jsonify({
            "message": "user_id is required"
        }), 400

    if not isinstance(items, list) or not items:
        return jsonify({
            "message": "items must be a non-empty list"
        }), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    try:
        order = Order(
            user_id=user_id,
            total=0,
            status="pending"
        )

        db.session.add(order)

        total = 0

        for item_data in items:
            if not isinstance(item_data, dict):
                db.session.rollback()

                return jsonify({
                    "message": "Each item must be an object"
                }), 400

            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity")

            if product_id is None:
                db.session.rollback()

                return jsonify({
                    "message": "product_id is required"
                }), 400

            if not isinstance(quantity, int) or quantity <= 0:
                db.session.rollback()

                return jsonify({
                    "message": "quantity must be a positive integer"
                }), 400

            product = Product.query.get(product_id)

            if not product:
                db.session.rollback()

                return jsonify({
                    "message": f"Product {product_id} not found"
                }), 404

            if product.stock < quantity:
                db.session.rollback()

                return jsonify({
                    "message": f"Insufficient stock for product {product_id}"
                }), 400

            item_price = product.price
            item_total = item_price * quantity
            total += item_total

            product.stock -= quantity

            order_item = OrderItem(
                order=order,
                product_id=product_id,
                quantity=quantity,
                price=item_price
            )

            db.session.add(order_item)

        order.total = total

        db.session.commit()

        return jsonify({
            "id": order.id,
            "user_id": order.user_id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": float(item.price)
                }
                for item in order.order_items
            ]
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Failed to create order",
            "error": str(e)
        }), 500


@main.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Request body is required"
        }), 400

    if "status" in data:
        status = data.get("status")

        allowed_statuses = [
            "pending",
            "processing",
            "completed",
            "cancelled"
        ]

        if status not in allowed_statuses:
            return jsonify({
                "message": "Invalid order status"
            }), 400

        order.status = status

    try:
        db.session.commit()

        return jsonify({
            "id": order.id,
            "user_id": order.user_id,
            "total": float(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat()
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500


@main.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }), 404

    try:
        for item in list(order.order_items):
            product = Product.query.get(item.product_id)

            if product:
                product.stock += item.quantity

            db.session.delete(item)

        db.session.delete(order)
        db.session.commit()

        return jsonify({
            "message": "Order deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500
