```
# 🚀 Project Management REST API

A production-ready **Project Management REST API** built with **FastAPI, PostgreSQL, and SQLAlchemy**, designed using a clean layered architecture (Router → Service → Repository).

---

## ⚙️ Tech Stack

- FastAPI
- PostgreSQL 15
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Docker & Docker Compose

---

## 🏗 Architecture

```

Client
↓
Routers (HTTP layer only)
↓
Services (Business logic + validation)
↓
Repositories (Database access layer)
↓
PostgreSQL

```

### Key Idea
- Routers → only request/response handling  
- Services → business rules + ownership checks  
- Repositories → all DB queries (no logic here)

---

## 📦 Features

- User registration & login (JWT auth)
- Secure password hashing (bcrypt)
- Project management (CRUD)
- Task management with status tracking
- Role/ownership-based access control
- Clean layered architecture (scalable design)
- Seed data for quick testing
- Dockerized setup

---

## 🗄 Database Schema

### User
- id
- email (unique)
- password_hash
- created_at
- updated_at

### Project
- id
- name
- description
- owner_id (FK → User)

### Task
- id
- title
- description
- status (TODO / IN_PROGRESS / DONE)
- due_date
- project_id (FK → Project)

---

## 🔐 Authentication Flow

1. Register user → `POST /api/auth/register`
2. Login user → `POST /api/auth/login`
3. Receive JWT token (60 min expiry)
4. Use token in headers:

```

Authorization: Bearer <token>

````

All protected routes validate ownership before access.

---

## 🚀 Run the Project

### Using Docker (Recommended)

```bash
docker-compose up --build
````

* API → [http://localhost:8000](http://localhost:8000)
* Docs → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Test Credentials

```
Email: test@example.com
Password: Password123
```

Includes:

* Sample project
* Sample tasks (TODO / IN PROGRESS / DONE)

---

## 📡 API Overview

### Auth

**Register**

```
POST /api/auth/register
```

**Login**

```
POST /api/auth/login
```

---

### User

**Get Profile**

```
GET /api/users/me
```

---

### Projects & Tasks

* CRUD for projects
* CRUD for tasks under projects
* Task status tracking
* Ownership validation enforced

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🧱 Design Highlights

* Clean separation of concerns (Router → Service → Repository)
* No direct DB access in routers
* Scalable structure for large systems
* Easy to extend (microservice-ready style)

---

## 📈 Possible Improvements

* Pagination for large datasets
* Role-based access control (Admin/User)
* Redis caching layer
* Async database optimization
* Centralized logging + monitoring

---

## 📌 Summary

This project focuses on **real-world backend structure**, clean architecture, and production-ready API design using FastAPI + PostgreSQL.

```
```
