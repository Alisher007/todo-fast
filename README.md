🚀 FastAPI Todo App
Welcome to the FastAPI Todo App! This project demonstrates a robust and well-structured API for managing your tasks, built with FastAPI, SQLModel (for database interactions), and a strong focus on Test-Driven Development (TDD).

✨ Features
Create, Read, Update, Delete (CRUD) Todo items.
Database Persistence: Uses SQLModel with SQLite for reliable data storage.
Automatic Interactive API Documentation: Powered by Swagger UI (/docs) and ReDoc (/redoc).
Robust Testing: Comprehensive test suite using Pytest and FastAPI TestClient, following TDD principles.
Pydantic Models: Strong data validation and serialization/deserialization.
Dependency Injection: Efficient handling of database sessions.
🛠️ Technologies Used
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
SQLModel: A library for interacting with SQL databases, designed to be easy to use and compatible with FastAPI. It's built on top of Pydantic and SQLAlchemy.
Uvicorn: A lightning-fast ASGI server for running your FastAPI application.
Pytest: A popular and powerful testing framework for Python.
Httpx: A modern, asynchronous HTTP client, used internally by FastAPI's TestClient.
⚙️ Setup and Installation
Follow these steps to get your Todo app up and running on your local machine.

1. Clone the Repository
First, clone this repository to your local machine:

Bash

git clone [<repository-url>](https://github.com/Alisher007/todo-fast.git)
cd todo-fast
2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies. This project uses uv for environment management, which is a fast and modern alternative.

Bash

uv venv
source .venv/bin/activate # On macOS/Linux
# Or for Windows: .venv\Scripts\Activate.ps1 (PowerShell) or .venv\Scripts\activate.bat (Command Prompt)
3. Install Dependencies
Once your virtual environment is active, install the required packages:

Bash

uv pip install fastapi "uvicorn[standard]" sqlmodel pytest httpx
4. Initialize the Database
The application uses SQLite, which stores data in a file (todos.db). You need to create the database file and its tables once before running the application for the first time.

Bash

python -c "from main import create_db_and_tables; create_db_and_tables()"
🚀 Running the Application
To start the FastAPI development server:

Bash

uvicorn main:app --reload
The --reload flag is useful during development, as it automatically restarts the server when code changes are detected.

Once the server is running, you can access the API at http://127.0.0.1:8000.

API Documentation
FastAPI automatically generates interactive API documentation:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
You can use these interfaces to explore and test the API endpoints directly in your browser.

✅ Running Tests (TDD in Action!)
This project follows a Test-Driven Development approach. To run the comprehensive test suite:

Ensure your virtual environment is active and you are in the project's root directory (todo-fast/).

Bash

PYTHONPATH=. pytest tests/
This command runs all tests located in the tests/ directory. The PYTHONPATH=. part ensures that Python can correctly locate your main.py module during testing.

📂 Project Structure
todo-fast/
├── .venv/                   # Virtual environment directory
├── __init__.py              # Makes 'todo-fast' a Python package (useful for pytest)
├── main.py                  # Main FastAPI application and API endpoints
├── todos.db                 # SQLite database file (created on startup)
├── tests/
│   └── test_main.py         # Pytest test suite for API endpoints
├── README.md                # This file!
└── requirements.txt         # (Optional: for listing dependencies)
🤝 Contributing
Contributions are welcome! If you have suggestions or find issues, please open an issue or submit a pull request.