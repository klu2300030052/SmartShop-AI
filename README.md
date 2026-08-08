# 🛒 SmartShop AI

## AI-Powered E-Commerce Product Recommendation System

---

# 👨‍💻 Team Details

| Role | Details |
|------|---------|
| **Team ID** | **T183** |
| **Team Lead** | Attanti Sri Swetha (2300030052) |
| **Member 1** | Godavarthi Chaturya (2300090016) |
| **Member 2** | Harshwardhan Raj (2300090312) |
| **Room** | R705B |

---

# 📖 Project Overview

SmartShop AI is an AI-powered e-commerce product recommendation system developed for the AI Build Placement Hackathon 2026.

The application enables users to create an account, log in, search products using AI-assisted fuzzy matching (RapidFuzz), browse categories, explore trending products, view product details, manage shopping carts and wishlists, and enjoy a responsive shopping experience built with Flask.

---

# 🎯 Problem Statement

Build an AI-powered shopping platform that recommends products and provides an intelligent, user-friendly online shopping experience.

---

# 💡 Solution

SmartShop AI uses RapidFuzz-based intelligent search to provide relevant product recommendations based on user queries. The application also offers product browsing, category navigation, shopping cart management, wishlist management, and an interactive web interface.

---

# ✨ Features

- 🔐 User Login & Signup
- 🔍 AI Product Search
- 🤖 AI Product Recommendation
- 🛍️ Product Details Page
- ❤️ Wishlist (Add & Remove)
- 🛒 Shopping Cart (Add & Remove)
- 📂 Categories
- 🔥 Trending Products
- 🖼️ Product Images
- ⚡ Fast Search using RapidFuzz
- 🎨 Responsive User Interface
- 🚪 Logout
- 🖥️ Flask Backend

---

# 🛠️ Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## AI / Libraries

- Pandas
- RapidFuzz
- NumPy

---

# 🏗️ System Architecture

```text
                    +----------------------+
                    |        User          |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Login / Signup       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Home Page            |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Search Interface     |
                    | (HTML/CSS/JS)        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Flask Backend        |
                    | (app.py)             |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Recommendation Engine|
                    | (recommender.py)     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Product Dataset      |
                    | (products.csv)       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Search Results       |
                    +----------------------+
```

---

# 🔄 System Workflow

```text
                User
                  │
                  ▼
          Login / Signup
                  │
                  ▼
            Home Page
                  │
                  ▼
          Search Products
                  │
                  ▼
         View Product Details
          │        │        │
          │        │        │
          ▼        ▼        ▼
     Add to Cart Wishlist Categories
                  │
                  ▼
          Trending Products
                  │
                  ▼
               Logout
```

---

# 📁 Folder Structure

```text
AI-Build-Hackathon
│
├── backend
│   ├── app.py
│   ├── recommender.py
│   ├── requirements.txt
│   ├── templates
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── product.html
│   │   ├── cart.html
│   │   ├── wishlist.html
│   │   ├── categories.html
│   │   └── trending.html
│   │
│   └── static
│       ├── css
│       └── product_images
│
├── dataset
│   └── products.csv
│
└── README.md
```

---

# ▶️ How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

# 📷 Application Modules

- Login
- Signup
- Home Page
- Product Search
- Product Details
- Shopping Cart
- Wishlist
- Categories
- Trending Products
- Logout

---

# 🚀 Future Enhancements

- Personalized AI Recommendations
- AI Chatbot Assistant
- Voice Search
- Payment Gateway Integration
- Order Tracking
- Purchase History
- Cloud Deployment

---

# 👥 Team Members

| Roll No | Name | Department |
|---------|------|------------|
| 2300030052 | Attanti Sri Swetha | HTE |
| 2300090016 | Godavarthi Chaturya | CS&IT |
| 2300090312 | Harshwardhan Raj | HTI |

---

# 🎯 Developed For

**AI Build Placement Hackathon 2026**

**KL University**

---



© 2026 SmartShop AI Team – T183