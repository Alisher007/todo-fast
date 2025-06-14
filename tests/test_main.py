# tests/test_main.py

# CHANGE THIS LINE:
# from httpx import Client
# TO THIS:
from fastapi.testclient import TestClient

from main import app, todos_db
import pytest

# Initialize the TestClient correctly
# CHANGE THIS LINE:
# client = Client(app=app)
# TO THIS:
client = TestClient(app) # Note: no keyword argument 'app', just pass the app instance

# Helper to clear the in-memory database before each test involving it
@pytest.fixture(autouse=True)
def clear_todos_db():
    """Clears the in-memory todos_db before each test."""
    todos_db.clear()
    yield
    todos_db.clear()

def test_read_root():
    """
    Test that the root endpoint returns the correct welcome message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to your FastAPI Todo App!"}

def test_create_todo():
    """
    Test that a new todo item can be created successfully.
    """
    todo_data = {"title": "Learn FastAPI"}
    response = client.post("/todos/", json=todo_data)

    response_data = response.json()
    assert "id" in response_data  # Check if 'id' key exists
    assert isinstance(response_data["id"], int) # Check if 'id' is an integer
    assert response_data["title"] == "Learn FastAPI"
    assert response_data["completed"] == False
    assert len(todos_db) == 1
    assert todos_db[0].title == "Learn FastAPI"
    assert todos_db[0].completed == False
    assert todos_db[0].id == 0 # Since it's the first one, we expect id 0

def test_create_todo_invalid_data():
    """
    Test that creating a todo with invalid data returns a 422 error.
    """
    invalid_todo_data = {"not_a_title": "Invalid Todo"}
    response = client.post("/todos/", json=invalid_todo_data)

    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"][0]["loc"] == ["body", "title"]
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_get_all_todos_empty():
    """
    Test that retrieving all todos returns an empty list when no todos exist.
    """
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_all_todos_with_data():
    """
    Test that retrieving all todos returns the correct list of todos.
    """
    # Create some dummy todos first using the POST endpoint (or directly add to db)
    # Using the client.post simulates a real scenario, but for tests,
    # directly adding to todos_db might be faster if create_todo is already tested.
    # For now, let's stick to using the endpoint.
    client.post("/todos/", json={"title": "Buy milk"})
    client.post("/todos/", json={"title": "Walk the dog", "completed": True})

    response = client.get("/todos/")
    assert response.status_code == 200
    expected_todos = [
        {"id": 1, "title": "Buy milk", "completed": False},
        {"id": 2, "title": "Walk the dog", "completed": True}
    ]
    assert response.json() == expected_todos
    assert len(todos_db) == 2 # Verify our in-memory db reflects this

def test_get_single_todo():
    """
    Test that retrieving a single todo by ID returns the correct todo.
    """
    # Create a todo first to retrieve it
    client.post("/todos/", json={"title": "Do laundry"})
    # Assuming the first todo created gets ID 0 (based on list index for now)
    # This will change when we add proper IDs later, but for now, it's fine.
    todo_id = 3
    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json() == {"id": 3, "title": "Do laundry", "completed": False}

def test_get_single_todo_not_found():
    """
    Test that retrieving a non-existent todo returns a 404 Not Found error.
    """
    response = client.get("/todos/999") # Assuming 999 is an invalid ID
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"} # This is what FastAPI returns by default for 404 if you raise HTTPException

def test_update_todo():
    """
    Test that an existing todo item can be updated successfully.
    """
    # 1. Create a todo first
    client.post("/todos/", json={"title": "Original Title", "completed": False})
    todo_id = 4 # We know the ID of the first created item is 0

    # 2. Define the update data
    update_data = {"title": "Updated Title", "completed": True}

    # 3. Send a PUT request to update the todo
    response = client.put(f"/todos/{todo_id}", json=update_data)

    assert response.status_code == 200
    assert response.json() == {"id": 4, "title": "Updated Title", "completed": True}

    # 4. Verify the in-memory database is updated
    assert len(todos_db) == 1
    assert todos_db[0].title == "Updated Title"
    assert todos_db[0].completed == True


def test_update_todo_not_found():
    """
    Test that updating a non-existent todo returns a 404 Not Found error.
    """
    response = client.put("/todos/999", json={"title": "Non-existent"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo():
    """
    Test that an existing todo item can be deleted successfully.
    """
    # 1. Create a todo first
    client.post("/todos/", json={"title": "To be deleted"})
    todo_id = 5 # We know the ID of the first created item is 0

    # 2. Send a DELETE request
    response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully"}

    # 3. Verify the in-memory database is empty
    assert len(todos_db) == 1

    # 4. Try to get the deleted todo to confirm it's gone
    response_get = client.get(f"/todos/{todo_id}")
    assert response_get.status_code == 404

def test_delete_todo_not_found():
    """
    Test that deleting a non-existent todo returns a 404 Not Found error.
    """
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
