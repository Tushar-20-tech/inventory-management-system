
# 📦 Inventory Management System

A full-stack **Inventory Management System** built using **Django** that helps businesses efficiently manage products, track stock movements, and analyze inventory data with interactive dashboards.

---

## 🚀 Project Overview

This system allows users to:

- Manage products and categories
- Track stock inflow (Stock In) and outflow (Stock Out)
- Monitor real-time inventory levels
- Receive low stock alerts
- Visualize data using charts and analytics
- Maintain secure, user-specific data access

The project is designed with a **modern UI**, smooth animations, and **data-driven insights** to simulate a real-world ERP system.

---

## ✨ Key Features

### 🔐 Authentication System
- Secure user login & registration
- User-specific data isolation (multi-user support)

### 📦 Product Management
- Add, edit, delete products
- Category-based organization

### 📥 Stock In
- Add incoming stock
- Supplier & invoice tracking
- Automatic quantity update

### 📤 Stock Out
- Remove stock with validation
- Prevent negative stock errors
- Customer & reason tracking

### ⚠️ Low Stock Alerts
- Automatic detection of low inventory
- Highlighted warnings on dashboard

### 📊 Dashboard Analytics
- Total Products
- Total Stock
- Low Stock Count
- Quick insights

### 📈 Reports & Charts
- 📊 Bar Graph (Stock comparison)
- 🥧 Pie Chart (Category distribution)
- 📡 Radar Chart (Inventory analysis)

### 🎨 UI/UX
- Smooth animations
- Responsive layout
- Professional dashboard design

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js
- **Database:** SQLite



---

## 🔒 Security Features

- User-based data filtering
- Each user can access only their own inventory
- Protected CRUD operations

---

## 📂 Project Structure
inventory_management/
│
├── main/
│ ├── models.py
│ ├── views.py
│ ├── templates/
│ └── static/
│
├── inventory_management/
│ ├── settings.py
│ └── urls.py
│
├── db.sqlite3
└── manage.py


---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/Tushar-20-tech/inventory-management-system.git
cd inventory-management-system

2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows


3. Install Dependencies
pip install django

4. Run Migrations
python manage.py makemigrations
python manage.py migrate

5. Run Server
python manage.py runserver

6. Open in Browser
http://127.0.0.1:8000/

<img width="1880" height="767" alt="inv2" src="https://github.com/user-attachments/assets/123a1496-cb5e-4e6c-ab27-05285af448a4" />

