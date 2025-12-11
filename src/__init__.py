from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_route
from src.auth.routers import auth_router
from src.db.db_agent import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server Started .....")
    await init_db()
    yield
    print("Server Closed .....")

version = "v1"

app = FastAPI(
    title="Secure Media Server",
    summary="A FastAPI secured server to demo the backend functionality of a Social Media Application",
    version=version,
    lifespan=life_span
)
app.include_router(router=book_route, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(router=auth_router, prefix=f"/api/{version}/auth", tags=["auth"])


@app.get("/")
async def main():
    return {"message": "Welcome"}