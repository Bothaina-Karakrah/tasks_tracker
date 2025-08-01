# ``
from fastapi import FastAPI
from app.routers import tasks, users, categories


app = FastAPI(title="Task Manager API")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(categories.router)