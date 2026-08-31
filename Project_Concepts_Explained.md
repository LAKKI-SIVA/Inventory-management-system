# Project Concepts & Technologies Explained

This document is a comprehensive guide to help you explain **why** specific technologies, architectural patterns, and design decisions were used in this Inventory Management System. Use this as a cheat sheet for interviews or presentations!

---

## 1. Architectural Pattern: Modular Monolith
**What is it?** A single, unified application where the code is strictly separated into independent "apps" or modules (Accounts, Products, Orders, Inventory).
**Why did we use it?**
- **Simplicity & Speed:** Microservices are too complex for a standard inventory system. They require managing multiple servers, complex networking, and distributed databases.
- **Maintainability:** By keeping modules strictly separated inside one codebase, the code is highly organized. If we ever need to extract `Orders` into its own microservice in the future, it will be very easy because the code is already decoupled.

---

## 2. Framework: Django (Python)
**What is it?** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
**Why did we use it?**
- **"Batteries Included":** Django provides built-in authentication, an Admin dashboard, and an ORM out of the box. This saved us hundreds of hours of writing boilerplate code.
- **Security:** Django automatically protects against common vulnerabilities like SQL Injection, Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF).

---

## 3. Database: PostgreSQL
**What is it?** An advanced, open-source relational database management system (RDBMS).
**Why did we use it instead of SQLite or MongoDB?**
- **SQLite is for toys:** SQLite locks the entire database when writing data. If two users try to save an order at the exact same time, SQLite crashes. PostgreSQL handles thousands of concurrent users perfectly.
- **ACID Compliance & Data Integrity:** Inventory data involves money and stock levels. PostgreSQL guarantees that transactions (like deducting stock and saving a receipt) either completely succeed or completely fail together (`@transaction.atomic`), preventing data corruption.
- **Not MongoDB:** Inventory data is strictly relational (An Order -> belongs to -> A Customer -> contains -> Products). Relational databases (SQL) are the industry standard for this.

---

## 4. Backend Design Patterns
### A. The "Service Layer" Pattern
**What is it?** Moving business logic out of the `views.py` and into a separate `services.py` file.
**Why did we use it?**
- **Reusability:** If you need to deduct stock when a user places an order via the API *and* via the HTML website, both views can just call `inventory.services.deduct_stock()`. 
- **Testing:** It is much easier to write automated tests for a single Python function in `services.py` than to fake web requests to test a `view.py`.

### B. Django Signals
**What is it?** A system that allows decoupled applications get notified when actions occur elsewhere in the framework.
**Why did we use it?**
- **Audit Trails:** Whenever an Inventory Stock is saved, a Signal silently catches that event and writes a log to the database. The core business logic doesn't even know the logging is happening, keeping the code clean.

---

## 5. Security: JWT (JSON Web Tokens)
**What is it?** A compact, URL-safe means of representing claims to be transferred between two parties.
**Why did we use it?**
- **Stateless Authentication:** For our REST APIs, JWT allows the server to verify who the user is without having to query the database or store session data in memory. This makes the APIs extremely fast and scalable.

---

## 6. Infrastructure: Docker & Nginx
### A. Docker
**What is it?** A platform that packages an application and all its dependencies into a standardized unit called a container.
**Why did we use it?**
- **"It works on my machine" is solved:** Docker ensures that the Django code, Python version, and PostgreSQL database run exactly the same way on your Windows laptop as they do on a Linux production server.

### B. Nginx
**What is it?** A high-performance web server and reverse proxy.
**Why did we use it?**
- **Static File Serving:** Django/Gunicorn is great at running Python logic, but it is very slow at serving CSS files and images. Nginx sits in front, instantly hands the user the CSS files, and only wakes up Django when complex Python logic is needed. 
- **Security:** Nginx acts as a shield, hiding the internal Django server from the public internet.
