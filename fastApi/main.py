from fastapi import FastAPI, HTTPException, status

app = FastAPI()


cursos = {
    1: {"titulo": "Inicial", "aulas": 112, "horas": 58},
    2: {"titulo": "Segundo", "aulas": 100, "horas": 20},
}


@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{id}")
async def get_curso(id: int):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
