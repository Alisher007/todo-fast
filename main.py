# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 1. Define the Pydantic Model for a Todo Item
class TodoItem(BaseModel):
    id: Optional[int] = None # ID will be assigned by the server
    title: str
    completed: bool = False

# In-memory "database" for now.
# Use a list to store TodoItem objects.
todos_db: List[TodoItem] = []
next_todo_id: int = 0 # Simple counter for IDs

@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI Todo App!"}

# Endpoint to create a new Todo item (POST request)
@app.post("/todos/", response_model=TodoItem) # Add response_model for better OpenAPI docs
def create_todo(todo: TodoItem):
    global next_todo_id # We need to use 'global' to modify the global variable
    todo.id = next_todo_id
    next_todo_id += 1
    todos_db.append(todo)
    return todo # Return the created todo item (with its ID)

# 3. New Endpoint: Get all Todo items
@app.get("/todos/", response_model=List[TodoItem]) # Specify the response model is a list of TodoItem
def read_todos():
    return todos_db

# 4. New Endpoint: Get a single Todo item by ID
@app.get("/todos/{todo_id}", response_model=TodoItem)
def read_todo(todo_id: int): # FastAPI automatically validates todo_id as an integer
    # Find the todo in our in-memory list by its ID
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    # If not found, raise an HTTPException (FastAPI will convert to 404 JSON)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    # Find the todo by ID
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            # Update its properties. Ensure the ID remains the same.
            todos_db[index].title = updated_todo.title
            todos_db[index].completed = updated_todo.completed
            return todos_db[index] # Return the updated item
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}") # No response_model needed if returning a simple message
def delete_todo(todo_id: int):
    global todos_db # We might modify the list
    original_len = len(todos_db)
    # Filter out the todo with the matching ID
    todos_db = [todo for todo in todos_db if todo.id != todo_id]

    if len(todos_db) < original_len:
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")








