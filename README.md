# 🎓 Online Examination System (OES)

<p align="center">
  <a href="https://alijahan.pythonanywhere.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-PythonAnywhere-brightgreen?style=for-the-badge&logo=python&logoColor=white" alt="Live Demo" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </a>
  <a href="https://www.djangoproject.com/">
    <img src="https://img.shields.io/badge/Django-3.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  </a>
  <a href="https://www.sqlite.org/">
    <img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  </a>
  <a href="https://getbootstrap.com/">
    <img src="https://img.shields.io/badge/Frontend-Bootstrap%204-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  </a>
</p>

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Live Application Access](#-live-application-access)
3. [System Analysis & Design (SAD) Diagrams](#-system-analysis--design-sad-diagrams)
   - [1. System Architecture (3-Tier)](#1-system-architecture-3-tier)
   - [2. Use Case Diagram](#2-use-case-diagram)
   - [3. Entity-Relationship Diagram (ERD)](#3-entity-relationship-diagram-erd)
4. [Key Features](#-key-features)
   - [Student Module](#student-module)
   - [Teacher Module](#teacher-module)
   - [Admin Module](#admin-module)
5. [Local Development Setup (VS Code)](#-local-development-setup-vs-code)
6. [Deployment Guide (PythonAnywhere)](#-deployment-guide-pythonanywhere)
7. [Database Structure](#-database-structure)
8. [Author & License](#-author--license)

---

## 📖 Project Overview

The **Online Examination System (OES)** is a web-based portal developed using **Python** and **Django** as a term project for the **System Analysis and Design (SAD)** course at **Daffodil International University**. 

The system digitizes and automates the traditional examination process by offering role-based portals for Students, Teachers, and Administrators. It allows instructors to manage MCQ question banks and enables students to take exams online with automated score calculation.

---

## 🌐 Live Application Access

The project is deployed and live on PythonAnywhere:

- 🌐 **Live Website**: [https://alijahan.pythonanywhere.com/](https://alijahan.pythonanywhere.com/)
- ⚙️ **Hosting**: PythonAnywhere WSGI Server
- 🛡️ **Security**: Django Authentication & CSRF Protection

---

## 📐 System Analysis & Design (SAD) Diagrams

### 1. System Architecture (3-Tier)

The application follows a standard **3-Tier Architecture** implemented through Django's Model-View-Template (MVT) design pattern.

```mermaid
graph TB
    subgraph PresentationTier["Presentation Layer (Client)"]
        UI["Web Browser Interface"]
        Templates["HTML5 / CSS3 Templates"]
        Bootstrap["Bootstrap 4 UI"]
    end

    subgraph ApplicationTier["Application Layer (Django Web Server)"]
        URL["URL Dispatcher"]
        AuthMiddleware["Authentication & Session Middleware"]
        Views["View Controllers (MVT)"]
        ScoreEngine["Automated MCQ Evaluation Engine"]
    end

    subgraph DataTier["Data Layer (Persistence)"]
        ORM["Django ORM Engine"]
        Database[("SQLite3 Relational Database")]
    end

    UI -->|HTTP GET / POST| URL
    URL --> AuthMiddleware
    AuthMiddleware --> Views
    Views --> ScoreEngine
    Views <-->|Database Query| ORM
    ORM <-->|SQL Operations| Database
    Views -->|Response HTML| Templates
    Templates -->|Render Page| UI
```

---

### 2. Use Case Diagram

Standard UML Use Case Diagram representing functional interactions between system actors (**Student**, **Teacher**, **Administrator**) and core system boundaries.

```mermaid
graph LR
    subgraph SystemActors["System Actors"]
        Student(("Student"))
        Teacher(("Teacher"))
        Admin(("Administrator"))
    end

    subgraph SystemBoundary["Online Examination System"]
        UC1["Account Registration & Login"]
        UC2["Approve Teacher Account"]
        UC3["Manage Teacher Details & Salary"]
        UC4["Manage Student Records"]
        UC5["Create Exam Course"]
        UC6["Add MCQ Questions"]
        UC7["Attend Online Exam"]
        UC8["Calculate Score Automatically"]
        UC9["View Marks & Scorecard"]
    end

    Student --> UC1
    Student --> UC7
    Student --> UC8
    Student --> UC9

    Teacher --> UC1
    Teacher --> UC5
    Teacher --> UC6

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC9
```

---

### 3. Entity-Relationship Diagram (ERD)

The conceptual entity-relationship model defines database entity attributes, primary/foreign keys, and relational cardinalities across the system.

```mermaid
erDiagram
    USER ||--|| STUDENT : "extends"
    USER ||--|| TEACHER : "extends"
    COURSE ||--|{ QUESTION : "contains"
    STUDENT ||--|{ RESULT : "attempts"
    COURSE ||--|{ RESULT : "evaluates"

    USER {
        int id PK
        string username
        string first_name
        string last_name
        string email
        string password
    }

    STUDENT {
        int id PK
        int user_id FK
        string profile_pic
        string mobile
        string address
    }

    TEACHER {
        int id PK
        int user_id FK
        string profile_pic
        string mobile
        string address
        boolean status
        int salary
    }

    COURSE {
        int id PK
        string course_name
        int question_number
        int total_marks
    }

    QUESTION {
        int id PK
        int course_id FK
        int marks
        string question
        string option1
        string option2
        string option3
        string option4
        string answer
    }

    RESULT {
        int id PK
        int student_id FK
        int exam_id FK
        int marks
        datetime date
    }
```

---

## ⚡ Key Features

### Student Module
- **Registration & Authentication**: Students can sign up and log in securely.
- **Course Selection**: Browse available exam courses and view exam guidelines.
- **Online MCQ Examination**: Attend timed multiple-choice question tests online.
- **Instant Result Evaluation**: Automated score calculation upon test submission.
- **Marksheet & History**: Track performance history and marks achieved across different exams.

### Teacher Module
- **Instructor Signup**: Register as a teacher (requires administrative account verification).
- **Course Management**: Add and manage exam subjects along with total question count and marks.
- **Question Bank Curation**: Add MCQs with 4 options and set the correct option key.
- **View Assigned Questions**: Inspect questions linked to created exam modules.

### Admin Module
- **Teacher Account Approval**: Approve or decline newly registered teacher accounts.
- **Salary Management**: Assign and manage salaries for verified teachers.
- **Student & Teacher Audit**: View and manage enrolled student and teacher profiles.
- **Exam & Question Governance**: Add or remove courses, questions, and manage question sets.
- **Institution Marksheets**: Audit student examination performance and overall marksheets.

---

## 💻 Local Development Setup (VS Code)

### Prerequisites
- Python 3.8 or higher installed on your PC.
- Git version control installed.
- VS Code editor.

### Step-by-Step Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alijahan365/Online-Examination-System.git
   cd Online-Examination-System
   ```

2. **Create & Activate Virtual Environment**
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Admin Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Local Server**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` in your browser.

---

## ☁️ Deployment Guide (PythonAnywhere)

The application is deployed on **PythonAnywhere** at `https://alijahan.pythonanywhere.com/`.

1. **Upload Code**: Clone repository into PythonAnywhere Bash console.
2. **Create Virtualenv**: Set up Python virtual environment (`mkvirtualenv --python=/usr/bin/python3.10 oes-env`) and install `requirements.txt`.
3. **Migrate & Collect Static Files**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. **WSGI Setup**: Configure WSGI file (`onlinexam/wsgi.py`) pointing to your project directory.
5. **Static Mappings**: Set `/static/` pointing to `/home/alijahan/Online-Examination-System/static/`.
6. **Reload**: Reload the Web app from PythonAnywhere dashboard.

---

## 🗄️ Database Structure

```text
+------------------+          +-------------------+          +------------------+
|     Student      |          |       User        |          |     Teacher      |
+------------------+          +-------------------+          +------------------+
| id               | 1      1 | id                | 1      1 | id               |
| user_id (FK)     |<-------->| username          |<-------->| user_id (FK)     |
| profile_pic      |          | first_name        |          | profile_pic      |
| mobile           |          | email             |          | status           |
| address          |          +-------------------+          | salary           |
+--------+---------+                                         +------------------+
         | 1
         |
         | N
+--------v---------+          +-------------------+          +------------------+
|      Result      |          |      Course       |          |     Question     |
+------------------+          +-------------------+          +------------------+
| id               | N      1 | id                | 1      N | id               |
| student_id (FK)  |<-------->| course_name       |<-------->| course_id (FK)   |
| exam_id (FK)     |          | question_number   |          | question         |
| marks            |          | total_marks       |          | option1..option4 |
| date             |          +-------------------+          | answer           |
+------------------+                                         +------------------+
```

---

## 👨‍💻 Author & License

<p align="center">
  <b>Developed by</b>: Ali Jahan <br>
  <b>Course</b>: System Analysis and Design (SAD) <br>
  <b>University</b>: Daffodil International University <br>
  <b>Live Site</b>: <a href="https://alijahan.pythonanywhere.com/">alijahan.pythonanywhere.com</a>
</p>

---

Copyright © 2026 Ali Jahan. All rights reserved.  
*Developed for academic evaluation at Daffodil International University.*
