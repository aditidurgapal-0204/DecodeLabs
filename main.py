from fastapi import FastAPI
import database
import project1
import project2
import project3
import project4

app = FastAPI(title="Industrial Internship Workspace")

# Automatically generate database tables inside vault.db on initialization
database.Base.metadata.create_all(bind=database.engine)

# Mount all 4 modular industrial assignment routers
app.include_router(project1.router, tags=["Project 1: REST Fundamentals"])
app.include_router(project2.router, tags=["Project 2: Database Integration"])
app.include_router(project3.router, tags=["Project 3: Secure Authentication"])
app.include_router(project4.router, tags=["Project 4: Third-Party API Integration"])