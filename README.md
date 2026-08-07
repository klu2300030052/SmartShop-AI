# 🛒 SmartShop AI

## AI Build Placement Hackathon 2026

### AI Powered Product Recommendation System

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

SmartShop AI is an AI-powered product recommendation system developed for the AI Build Placement Hackathon 2026.

The application allows users to search for products and instantly receive intelligent recommendations using fuzzy string matching (RapidFuzz). It provides a simple, fast, and interactive shopping experience through a Flask-based web application.

---

# ✨ Features

- 🔍 AI Product Search
- 🤖 Product Recommendation
- ⚡ Fast Search using RapidFuzz
- 🎨 User-Friendly Interface
- 🖥️ Flask Backend
- 📂 CSV Product Dataset
- 📱 Responsive Design

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
                    | Recommended Results  |
                    +----------------------+
```

---

# 🔄 System Workflow

```text
              Start
                 │
                 ▼
        User Opens Website
                 │
                 ▼
       Enter Product Name
                 │
                 ▼
          Click Search
                 │
                 ▼
      Flask Receives Request
                 │
                 ▼
 RapidFuzz Searches Dataset
                 │
                 ▼
 Matching Products Found
                 │
                 ▼
 Display Search Results
                 │
                 ▼
                End
```

---

# 📁 Folder Structure

```text
AI-Build-Hackathon
│
├── backend
│   ├── app.py
│   ├── recommender.py
│   ├── templates
│   │   └── index.html
│   └── static
│       ├── css
│       ├── js
│       └── images
│
├── dataset
│   └── products.csv
│
├── frontend
│
├── models
│
└── README.md
```

---

# 🚀 Future Enhancements

- Sentence Transformers
- FAISS Vector Search
- AI Chatbot Assistant
- Voice Search
- Product Images
- User Login System
- Shopping Cart
- Personalized Recommendations

---

# 👥 Team Members

| Roll No | Name | Department |
|----------|------------------------|------------|
| 2300030052 | Attanti Sri Swetha | HTE |
| 2300090016 | Godavarthi Chaturya | CS&IT |
| 2300090312 | Harshwardhan Raj | HTI |

---

# 🎯 Developed For

**AI Build Placement Hackathon 2026**

**KL University**

---

© 2026 SmartShop AI Team – T183