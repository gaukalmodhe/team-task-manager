# 📌 Team Task Manager (Full Stack Project)

A Flask-based REST API application for managing teams, projects, and tasks with JWT authentication and role-based access control (Admin/Member). Deployed on Render.

---

# 🚀 Live Demo
https://team-task-manager-3-56gb.onrender.com

---

# 🧠 Project Overview
This project allows users to:
- Register and login securely
- Create and manage projects
- Create, assign, update, and delete tasks
- Track task status using dashboard

Role-based access:
- Admin → full control (projects + tasks)
- Member → view/update assigned tasks

---

# ⚙️ Features
- User Signup & Login (JWT Authentication)
- Role-Based Access Control
- Project Management
- Task Creation & Assignment
- Task Status Tracking
- Dashboard with statistics
- Secure password hashing (Bcrypt)
- SQLite Database

---

# 🛠️ Tech Stack
- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLite
- Render (Deployment)

---

# 📂 Project Structure
app.py  
requirements.txt  
README.md  

---

# 🔗 API Endpoints

## Authentication
POST /signup  
POST /login  

## Projects
POST /projects (Admin only)  
GET /projects  

## Tasks
POST /tasks (Admin only)  
GET /tasks  
PUT /tasks/<id>  
DELETE /tasks/<id>  

## Dashboard
GET /dashboard  

---

# 🔑 Authentication
Use JWT token in headers:

Authorization: Bearer <your_token>

---

# 🧪 Sample Requests

## Signup
```json
{
  "name": "Gaurav",
  "email": "modhe@gmail.com",
  "password": "992236",
  "role": "admin"
}

🚀 Run Locally
# Clone repository
git clone https://github.com/gaukalmodhe/team-task-manager.git

# Go to project folder
cd team-task-manager

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

🌐 Deployment
Hosted on Render
Auto deployment from GitHub
Live URL: https://team-task-manager-3-56gb.onrender.com⁠�

👨‍💻 Author
Gaurav Modhe

🏁 Conclusion
This project demonstrates:
REST API development
Authentication & Authorization
Role-based access control
Database management
Cloud deployment using Render

Thank you for reviewing this project 👍
