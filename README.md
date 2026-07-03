# DecodeLabs Industrial Internship Workspace

Welcome to my unified backend development repository. This single repository contains the complete implementation for **Projects 1, 2, 3, and 4**. 

Instead of writing separate, fragmented scripts, I have engineered these four modules into a cohesive, production-grade microservice architecture powered by **FastAPI**.

---

## 📁 Project Directory Map
When evaluating individual tasks, please refer to the corresponding files listed below:

* **Project 1: REST Fundamentals** (`project1.py`)
  * Handles stateless HTTP operations (GET, POST) using a dynamic in-memory data array representing a book inventory system.
* **Project 2: Database Integration** (`database.py`, `project2.py`, `vault.db`)
  * Implements a persistent relational database tier. Uses **SQLAlchemy ORM** to perform structured CRUD operations on a SQLite database file named `vault.db`.
* **Project 3: Secure Authentication** (`security.py`, `project3.py`, `.env`)
  * Implements secure access control using **Argon2id** (the industry standard for irreversible password hashing) and secure **JWT (JSON Web Tokens)**. It protects the sensitive `/dashboard` route using a stateless `HTTPBearer` authorization gatekeeper.
* **Project 4: Third-Party API Integration** (`project4.py`)
  * Establishes a secure asynchronous proxy gateway using **HTTPX** to fetch data from an external weather provider behind our server firewall. It strips away payload noise, normalizes fields, and provides runtime timeout shields to handle external server drops gracefully.

---

## ⚙️ Prerequisites & Environment Setup

Before running the server, you must install the required backend libraries. 

### 🚨 Critical Note for the Evaluator:
This is a modern web application framework that relies on an **Artificial ASGI Server Engine (Uvicorn)** to manage network traffic. It **cannot** be executed by clicking the generic VS Code "Play/Run" script button, as that button targets a blank system runtime path. It must be executed via the terminal workspace commands outlined below.

### Step 1: Install Dependencies
Open your terminal inside this project's root folder (`DecodeLabs`) and execute the following command to install all necessary packages:

```bash
pip install fastapi uvicorn sqlalchemy argon2-cffi pyjwt python-multipart httpx pydantic[email]
