from fastapi import FastAPI
import uvicorn

from router.breed import breed_router
from router.cats import cat_router

app = FastAPI(title="Test Task")

app.include_router(breed_router)
app.include_router(cat_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)