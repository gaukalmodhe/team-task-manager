# Install:
# Install flask flask_sqlalchemy flask_jwt_extended flask_bcrypt
#import sys
#print(sys.executable)
#!{sys.executable} -m pip install flask flask_sqlalchemy flask_jwt_extended flask_bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
from datetime import timedelta

# ==========================================
# APP CONFIG
# ==========================================

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# ==========================================
# DATABASE MODELS
# ==========================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))   # admin/member

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    status = db.Column(db.String(50), default="Pending")
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

# ==========================================
# HELPER FUNCTION
# ==========================================

def admin_required():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != "admin":
        return False

    return True

# ==========================================
# AUTH ROUTES
# ==========================================

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(
        data['password']
    ).decode('utf-8')

    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data['role']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })

# LOGIN
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(
        user.password,
        data['password']
    ):

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "role": user.role
        })

    return jsonify({
        "message": "Invalid credentials"
    }), 401


# ==========================================
# PROJECT ROUTES
# ==========================================

# CREATE PROJECT (ADMIN ONLY)
@app.route('/projects', methods=['POST'])
@jwt_required()
def create_project():

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()

    project = Project(
        title=data['title'],
        description=data['description']
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "message": "Project created successfully"
    })

# GET ALL PROJECTS
@app.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():

    projects = Project.query.all()

    output = []

    for p in projects:
        output.append({
            "id": p.id,
            "title": p.title,
            "description": p.description
        })

    return jsonify(output)

# ==========================================
# TASK ROUTES
# ==========================================

# CREATE TASK
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()

    task = Task(
        title=data['title'],
        description=data['description'],
        status=data['status'],
        assigned_to=data['assigned_to'],
        project_id=data['project_id']
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully"
    })

# GET TASKS
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():

    tasks = Task.query.all()

    output = []

    for t in tasks:
        output.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "assigned_to": t.assigned_to,
            "project_id": t.project_id
        })

    return jsonify(output)

# UPDATE TASK STATUS
@app.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    data = request.get_json()

    task.status = data['status']

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully"
    })

# DELETE TASK
@app.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):

    if not admin_required():
        return jsonify({"message": "Admin access required"}), 403

    task = Task.query.get(id)

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    })

# ==========================================
# DASHBOARD
# ==========================================

@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():

    total_tasks = Task.query.count()

    pending = Task.query.filter_by(status="Pending").count()

    completed = Task.query.filter_by(status="Completed").count()

    in_progress = Task.query.filter_by(status="In Progress").count()

    return jsonify({
        "total_tasks": total_tasks,
        "pending_tasks": pending,
        "completed_tasks": completed,
        "in_progress_tasks": in_progress
    })

# ==========================================
# MAIN
# ==========================================
@app.route('/')
def home():
    return "Team Task Manager API Running Successfully"

if __name__ == '__main__':

    
    app.run(debug=True)
#========================================
#Get Tasks
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():

    tasks = Task.query.all()

    result = []

    for t in tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "project_id": t.project_id,
            "assigned_to":t.assigned_to
        })

    return jsonify(result)

#===========================================
#Dashboard
#===========================================
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():

    total = Task.query.count()
    done = Task.query.filter_by(status="done").count()
    pending = Task.query.filter_by(status="pending").count()

    return jsonify({
        "total_tasks": total,
        "completed_tasks": done,
        "pending_tasks": pending
    })

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# API TESTING EXAMPLES
# ==========================================

"""
1. SIGNUP
POST /signup

{
    "name":"Admin",
    "email":"admin@gmail.com",
    "password":"1234",
    "role":"admin"
}

2. LOGIN
POST /login

{
    "email":"admin@gmail.com",
    "password":"1234"
}

3. CREATE PROJECT
POST /projects

Headers:
Authorization: Bearer TOKEN

{
    "title":"Website Project",
    "description":"Task Manager Project"
}

4. CREATE TASK
POST /tasks

{
    "title":"Frontend Design",
    "description":"Create UI",
    "status":"Pending",
    "assigned_to":1,
    "project_id":1
}

5. GET TASKS
GET /tasks

6. UPDATE TASK
PUT /tasks/1

{
    "status":"Completed"
}

7. DASHBOARD
GET /dashboard
"""