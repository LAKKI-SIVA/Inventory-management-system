# Database Credentials & Roles

This file contains the local database connection credentials for the Inventory Management System. Keep this for your permanent reference.

## 🐘 PostgreSQL Connection (Local Development)
These are the credentials used to connect your Django application to the local PostgreSQL database (via pgAdmin 4).

* **Database Engine:** PostgreSQL
* **Database Name:** `inventory_db`
* **Username / Role:** `postgres`
* **Password:** `postgres`
* **Host:** `127.0.0.1` (Localhost)
* **Port:** `5432`

## 🛡️ Django Superuser (Admin Panel)
If you haven't created an admin account yet to manage the inventory, run the following command in your terminal:
`python manage.py createsuperuser`

* **Username:** *(Whatever you choose, e.g., admin)*
* **Email:** *(Optional)*
* **Password:** *(Whatever you choose)*
* **Admin Login URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---
> **Security Note:** These are local development credentials. If you ever deploy this app to the internet (production), you will generate new, secure passwords that should not be written down in plain text files.
