# What is the Inventory Management System?

This project is a **Digital Inventory & Order Management Backend** built with Python and Django. 

Imagine a physical warehouse or retail store. They need a way to keep track of every item they own, who they bought it from, who they are selling it to, and exactly how many items are left on the shelves. **This project is the digital brain that handles all of that.**

### Core Features (What it actually does):

1. **Product Catalog:** It stores a digital list of every product, its price, its category (like Electronics or Clothing), and its image.
2. **Business Partners:** It keeps a directory of **Suppliers** (who you buy from) and **Customers** (who you sell to).
3. **Real-Time Stock Tracking:** It maintains a digital "Ledger" of how much stock is currently in the warehouse (`quantity_on_hand`) and warns you when stock gets dangerously low (`reorder_level`).
4. **Order Processing (The Magic):** When a Customer places an Order for 5 laptops, the system automatically and safely deducts 5 laptops from the inventory. It uses strict database rules to ensure it never accidentally sells a laptop it doesn't have.
5. **Security & Roles:** It uses strict security (JWT and Role-Based Access Control) to make sure a regular Customer can't log in and change the price of a product—only an Admin or Inventory Manager can do that.

### Why is this impressive?
Instead of a simple "Toy" app, this is built as an **Enterprise-Grade Modular Monolith**. 
- It has a beautiful **HTML Dashboard** for managers to look at.
- It also has a **REST API** so a mobile app developer could easily build an iOS/Android app that connects directly to this database.
- It uses **Docker**, meaning it is packaged up professionally and can be deployed to any server in the world with a single command.
