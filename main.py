# main.py

from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager

# --- Database Setup ---
DATABASE_URL = "sqlite:///./todos.db" # This will create a file named todos.db in your project directory
engine = create_engine(DATABASE_URL, echo=True) # echo=True logs SQL queries (useful for debugging)

def create_db_and_tables():
    """
    Creates the database tables based on SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)

# Dependency to get a database session for each request
# This handles opening and closing the session automatically
def get_session():
    with Session(engine) as session:
        yield session

# --- Lifespan Event Handler ---
# This replaces @app.on_event("startup") and @app.on_event("shutdown")
@asynccontextmanager # <--- Decorator for async context managers
async def lifespan(app: FastAPI): # <--- Define the lifespan function
    # Code that runs ON STARTUP
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created!")
    yield # <--- Application starts accepting requests here
    # Code that runs ON SHUTDOWN (optional, but good for cleanup)
    print("Shutting down...")
    # You might close connections or do other cleanup here if needed
    # For SQLite file, no explicit close needed for engine usually.

# --- FastAPI App Initialization ---
# Pass the lifespan function to the FastAPI constructor
app = FastAPI(lifespan=lifespan) # <--- Pass lifespan to FastAPI constructor
# --- TodoItem Model with SQLModel ---
class TodoItem(SQLModel, table=True): # table=True tells SQLModel this is a database table
    id: Optional[int] = Field(default=None, primary_key=True) # Primary key, auto-incrementing
    title: str = Field(index=True, nullable=False, min_length=1) # Add an index for faster lookups on title
    # <--- MODIFIED: Added min_length for Pydantic
    # and by default, str implies not nullable
    completed: bool = Field(default=False)


# --- FastAPI Endpoints (Refactored to use database session) ---
@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI Todo App!"}

# Create Todo
@app.post("/todos/", response_model=TodoItem)
def create_todo(*, todo: TodoItem, session: Session = Depends(get_session)):
    # Add a check here that should prevent the DB call if title is None
    if todo.title is None:
        print("ERROR: Todo title is None, but Pydantic should have caught this!")
        raise HTTPException(status_code=400, detail="Title cannot be None at this stage.")

    session.add(todo) # Add the todo object to the session
    session.commit() # Commit the transaction to save to DB
    session.refresh(todo) # Refresh the object to get its ID from the DB
    return todo

# Read All Todos
@app.get("/todos/", response_model=List[TodoItem])
def read_todos(*, session: Session = Depends(get_session)):
    todos = session.exec(select(TodoItem)).all() 
    return todos

# Read Single Todo
@app.get("/todos/{todo_id}", response_model=TodoItem)
def read_todo(*, todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoItem, todo_id) # Efficiently get by primary key
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update Todo
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(*, todo_id: int, todo_update: TodoItem, session: Session = Depends(get_session)):
    db_todo = session.get(TodoItem, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update attributes of the database object
    # We can use .model_dump(exclude_unset=True) to only update fields that were provided in the request
    # For now, we'll just update title and completed explicitly based on our current TodoItem model
    db_todo.title = todo_update.title
    db_todo.completed = todo_update.completed

    session.add(db_todo) # Add the updated object back to the session
    session.commit() # Commit the changes
    session.refresh(db_todo) # Refresh to ensure it has the latest state from DB
    return db_todo

# Delete Todo
@app.delete("/todos/{todo_id}")
def delete_todo(*, todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoItem, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo) # Delete the object
    session.commit() # Commit the deletion
    return {"message": "Todo deleted successfully"}