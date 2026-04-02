from fastapi import FastAPI
from routers import CombRouter, DrinkRouter

app = FastAPI()

# Include all your modular routers
app.include_router(CombRouter.router)
app.include_router(DrinkRouter.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Mixology API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
