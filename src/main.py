from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from src.database.database import Base, engine, SessionLocal
from src.routers import auth, users, projects, tasks
from src.core.security import get_password_hash
from src.models.user import User
from src.models.project import Project
from src.models.task import Task, TaskStatus

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management REST API",
    description="Production-grade Project Management API with strict layered architecture.",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

# Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error.get("loc", [])),
            "message": error.get("msg"),
            "type": error.get("type")
        })
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation Error", "errors": errors}
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    # Handle unique constraint violations gracefully
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database integrity conflict. Resource might already exist."}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Never expose stack traces in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."}
    )

# Seed Data Functionality
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # Check if test user already exists
        test_email = "test@example.com"
        user = db.query(User).filter(User.email == test_email).first()
        if not user:
            # Create Test User
            hashed_password = get_password_hash("Password123")
            user = User(email=test_email, password_hash=hashed_password)
            db.add(user)
            db.commit()
            db.refresh(user)

            # Create 1 Sample Project
            project = Project(
                name="Sample Project",
                description="This is a sample project created automatically.",
                owner_id=user.id
            )
            db.add(project)
            db.commit()
            db.refresh(project)

            # Create 3 Sample Tasks
            task1 = Task(
                title="Setup Project Architecture",
                description="Implement strict layered architecture with Repository Pattern.",
                status=TaskStatus.DONE,
                project_id=project.id
            )
            task2 = Task(
                title="Implement Authentication",
                description="Secure endpoints using JWT and bcrypt hashing.",
                status=TaskStatus.IN_PROGRESS,
                project_id=project.id
            )
            task3 = Task(
                title="Write Integration Tests",
                description="Verify all CRUD operations and ownership security rules.",
                status=TaskStatus.TODO,
                project_id=project.id
            )
            db.add_all([task1, task2, task3])
            db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()
