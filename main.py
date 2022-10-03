from fastapi import FastAPI
from routers import history, management, manager, user, vehicle

app = FastAPI()

app.include_router(user.router)
app.include_router(vehicle.router)
app.include_router(manager.router)
app.include_router(history.router)
app.include_router(management.router)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
