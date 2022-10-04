import time

from fastapi import FastAPI, Request
from routers import history, management, manager, user, vehicle


app = FastAPI()

app.include_router(user.router)
app.include_router(vehicle.router)
app.include_router(manager.router)
app.include_router(history.router)
app.include_router(management.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
