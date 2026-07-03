# DecodeLabs Industrial Internship Workspace

Welcome to my unified backend development repository. This single repository contains the complete implementation for Projects 1, 2, 3, and 4. 

Instead of writing separate, fragmented scripts, I have engineered these four modules into a cohesive, production-grade microservice architecture powered by FastAPI.

---

## 📁 Project Directory Map
When evaluating individual tasks, please refer to the corresponding files listed below:

* Project 1: REST Fundamentals (project1.py)
  - Handles stateless HTTP operations (GET, POST) using a dynamic in-memory data array representing a book inventory system.
* Project 2: Database Integration (database.py, project2.py, vault.db)
  - Implements a persistent relational database tier. Uses SQLAlchemy ORM to perform structured CRUD operations on a SQLite database file named vault.db.
* Project 3: Secure Authentication (security.py, project3.py, .env)
  - Implements secure access control using Argon2id (the industry standard for irreversible password hashing) and secure JWT (JSON Web Tokens). It protects the sensitive /dashboard route using a stateless HTTPBearer authorization gatekeeper.
* Project 4: Third-Party API Integration (project4.py)
  - Establishes a secure asynchronous proxy gateway using HTTPX to fetch data from an external weather provider behind our server firewall. It strips away payload noise, normalizes fields, and provides runtime timeout shields to handle external server drops gracefully.

---

## ⚙️ Prerequisites & Environment Setup

Before running the server, you must install the required backend libraries. 

### 🚨 Critical Note for the Evaluator:
This is a modern web application framework that relies on an ASGI Server Engine (Uvicorn) to manage network traffic. It CANNOT be executed by clicking the generic VS Code "Play/Run" script button, as that button targets a blank system runtime path. It must be executed via the terminal workspace commands outlined below.

### Step 1: Install Dependencies
Open your terminal inside this project's root folder (DecodeLabs) and execute the following installation command:

> pip install fastapi uvicorn sqlalchemy argon2-cffi pyjwt python-multipart httpx pydantic[email]

### Step 2: Set Up Environment Variables (.env)
A private configuration file named .env must exist in the root folder to house our secure system keys. If you are cloning this repository to a new machine, ensure a .env file is created in the root directory containing these exactly specified credentials:

> JWT_SECRET=super_secret_evaluation_signing_key_123
> WEATHER_API_KEY=fallback_local_dev_key

---

## 🚀 How to Run the Application

Once the packages are installed, execute the following command in your terminal to bring the entire 4-project workspace ecosystem online:

> python -m uvicorn main:app --reload

### 📋 Expected Terminal Output:
Upon execution, your terminal will confirm the runtime context and initialize the database models cleanly:

> INFO:     Will watch for changes in these directories: ['C:\Users\...\DecodeLabs']
> INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
> INFO:     Started reloader process [XXXX] using StatReload
> INFO:     Started server process [XXXX]
> INFO:     Waiting for application startup.
> INFO:     Application startup complete.

---

## 🔍 Testing the Projects Interactively

FastAPI compiles our entire codebase into an automated interactive dashboard documentation page. 

1. Ensure your terminal remains running with the command above.
2. Open your web browser and navigate to: http://127.0.0.1:8000/docs
3. You will see all 4 projects cleanly separated by visual category tags. 
4. Click "Try it out" on any endpoint (like /books, /users, or /weather/{city}) to run live operations and view response structures!

*(Note: For Project 3's protected dashboard route, use the global Authorize lock button at the top of the Swagger page to submit your generated JWT Bearer Token before testing).*
