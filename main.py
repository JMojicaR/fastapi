from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory "database" (for demo purposes)
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}

# Pydantic model for request/response validation
class User(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# ========== HTTP METHODS ========== #

# 1. GET (Retrieve all users)
@app.get("/users")
def get_users():
    return users_db

# 2. GET (Retrieve a single user)
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# 3. POST (Create a new user)
@app.post("/users")
def create_user(user: User):
    new_id = max(users_db.keys()) + 1
    users_db[new_id] = {"id": new_id, **user.dict()}
    return {"message": "User created", "user": users_db[new_id]}

# 4. PUT (Full update)
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = {"id": user_id, **user.dict()}
    return {"message": "User updated", "user": users_db[user_id]}

# 5. PATCH (Partial update)
@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored_user = users_db[user_id]
    update_data = user.dict(exclude_unset=True)  # Only updates provided fields
    updated_user = {**stored_user, **update_data}
    users_db[user_id] = updated_user
    return {"message": "User patched", "user": updated_user}

# 6. DELETE (Remove a user)
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users_db.pop(user_id)
    return {"message": "User deleted", "user": deleted_user}

# 7. HEAD (Same as GET but no body)
@app.head("/users/{user_id}")
def head_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404)
    return  # Returns headers only (no body)

# 8. OPTIONS (List allowed methods)
@app.options("/users")
def options_users():
    return {"Allow": "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS"}

# ========== Run the Server ========== #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)