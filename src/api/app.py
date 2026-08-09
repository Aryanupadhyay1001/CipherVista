from fastapi import FastAPI
from src.api.routes import router as main_router
from src.api.auth import router as auth_router
from src.core.config import settings
from src.database.database import engine, Base

# IMPORT MODELS SO SQLALCHEMY REGISTERS THEM FOR TABLE CREATION
from src.database.models import User, Report, ReportAttack, Investigation

# Auto-create database tables in PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Include Routers
app.include_router(main_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": f"{settings.PROJECT_NAME} API is Running",
        "database_connected": True
    }