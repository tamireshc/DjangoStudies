from fastapi import FastAPI
from routes import cursos_router


app = FastAPI(
    title="Api Cursos",
    version="0.0.1",
    description="Uma api para aprender fastapi",
)
app.include_router(cursos_router.router, tags=["cursos"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
