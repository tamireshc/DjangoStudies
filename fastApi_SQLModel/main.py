from fastapi import FastAPI

from src.controllers import curso_controller

from src.controllers import alunos_controller

app = FastAPI(
    title="Api Cursos",
    version="0.0.1",
    description="Uma api para aprender fastapi",
)

app.include_router(curso_controller.router, prefix="/cursos", tags=["cursos"])
app.include_router(alunos_controller.router, prefix="/alunos", tags=["alunos"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
