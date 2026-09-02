# API Documentation: Inventory Management System

This document outlines the RESTful API endpoints available in the system. All endpoints require JSON Web Token (JWT) authentication, except for the login and registration endpoints.

**Base URL**: `http://127.0.0.1:8000` (Local) / `https://your-domain.com` (Production)

---

## 1. Authentication (`/accounts/api/`)

You must authenticate to get a JWT Access Token. That token must be included in the header of all subsequent requests:
`Authorization: Bearer <your_access_token>`

### A. Login (Get Tokens)
- **Endpoint**: `POST /accounts/api/login/`
- **Description**: Submits credentials to receive an access and refresh token.
- **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:8000/accounts/api/login/ \
       -H "Content-Type: application/json" \
       -d '{"username": "admin", "password": "yourpassword"}'
  ```
- **Response**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs..."
  }
  ```

### B. Register New User
- **Endpoint**: `POST /accounts/api/register/`
- **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:8000/accounts/api/register/ \
       -H "Content-Type: application/json" \
       -d '{"username": "newuser", "password": "securepassword123", "email": "user@example.com"}'
  ```

---

## 2. Products (`/products/api/`)

### A. List All Products
- **Endpoint**: `GET /products/api/`
- **cURL Command**:
  ```bash
  curl -X GET http://127.0.0.1:8000/products/api/ \
       -H "Authorization: Bearer <your_access_token>"
  ```

### B. Create a Product
- **Endpoint**: `POST /products/api/`
- **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:8000/products/api/ \
       -H "Authorization: Bearer <your_access_token>" \
       -H "Content-Type: application/json" \
       -d '{
             "sku": "LAP-002",
             "name": "MacBook Pro",
             "description": "M2 Apple Laptop",
             "price": "1999.99",
             "category": 1,
             "supplier": 1
           }'
  ```

### C. Retrieve/Update/Delete a Single Product
- **Retrieve**: `GET /products/api/<id>/`
- **Update**: `PUT /products/api/<id>/`
- **Delete**: `DELETE /products/api/<id>/`
- **cURL Example (Retrieve)**:
  ```bash
  curl -X GET http://127.0.0.1:8000/products/api/1/ \
       -H "Authorization: Bearer <your_access_token>"
  ```

---

## 3. Categories & Suppliers

The same standard CRUD operations apply to Categories and Suppliers.

- **List Categories**: `GET /categories/api/`
- **Create Supplier**: `POST /suppliers/api/`
- **cURL Example (List Categories)**:
  ```bash
  curl -X GET http://127.0.0.1:8000/categories/api/ \
       -H "Authorization: Bearer <your_access_token>"
  ```

---

## 4. Inventory (`/inventory/api/`)

### A. View Stock Levels
- **Endpoint**: `GET /inventory/api/`
- **cURL Command**:
  ```bash
  curl -X GET http://127.0.0.1:8000/inventory/api/ \
       -H "Authorization: Bearer <your_access_token>"
  ```

### B. Adjust Stock manually
- **Endpoint**: `PUT /inventory/api/<stock_id>/`
- **cURL Command**:
  ```bash
  curl -X PUT http://127.0.0.1:8000/inventory/api/1/ \
       -H "Authorization: Bearer <your_access_token>" \
       -H "Content-Type: application/json" \
       -d '{"quantity": 100, "reorder_level": 20}'
  ```

---

## 5. Orders (`/orders/api/`)

### A. Place a New Order
- **Endpoint**: `POST /orders/api/`
- **Description**: Places an order and automatically deducts the quantity from the Inventory table using atomic transactions.
- **cURL Command**:
  ```bash
  curl -X POST http://127.0.0.1:8000/orders/api/ \
       -H "Authorization: Bearer <your_access_token>" \
       -H "Content-Type: application/json" \
       -d '{
             "customer": 1,
             "items": [
               { "product": 1, "quantity": 2 },
               { "product": 2, "quantity": 1 }
             ]
           }'
  ```
