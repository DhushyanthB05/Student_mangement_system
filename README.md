# 🎓 Smart Student Management System

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

A professional, production-ready Student Management System built with Python and Flask. This application evolved from a legacy Python CLI script into a full-stack, multi-tenant web application designed to handle student enrollments, academic tracking, and real-time analytics.

## ✨ Features

- **Role-Based Access Control (RBAC)**: Secure authentication with separate portals for Administrators (full CRUD access, analytics) and Students (read-only profile access).
- **Interactive Analytics Dashboard**: Real-time insights using **Chart.js**, visualizing academic performance distributions and department enrollments.
- **Bulk CSV Imports**: Effortlessly onboard hundreds of students at once via CSV uploads with built-in data validation.
- **Print-Ready PDF Generation**: Native support for exporting student profiles as official, print-ready academic transcripts.
- **Live Audit Logs**: A real-time activity feed that tracks all system modifications for security and compliance.
- **Modern UI/UX**: Premium Glassmorphism design, native Dark Mode toggle, smooth CSS animations, and fully responsive Bootstrap 5 components.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   `ash
   git clone https://github.com/YOUR_USERNAME/smart-student-management.git
   cd smart-student-management
   `

2. **Create and activate a virtual environment**
   `ash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   `

3. **Install dependencies**
   `ash
   pip install -r requirements.txt
   `

4. **Initialize the Database**
   This command will create the SQLite database, run the schema, and seed the initial admin account and dummy data.
   `ash
   flask --app run init-db
   `

5. **Run the Application**
   `ash
   flask --app run run --debug
   `
   Navigate to http://127.0.0.1:5000 in your browser.

## 🔐 Default Credentials
- **Admin Portal**: Username: Dhushyanth B | Password: 123456789
- **Student Portal**: Username: student1 | Password: password123

## 🛠️ Architecture
- **Backend**: Python, Flask, Flask-SQLAlchemy (ORM), Flask-Login (Auth), Flask-WTF (Forms & CSRF protection)
- **Frontend**: HTML5/Jinja2, Bootstrap 5.3, Chart.js, CSS3
- **Database**: SQLite

---
*Created by Dhushyanth B*
