from fastapi import FastAPI, HTTPException, Path, Response, status

from models import Curso

app = FastAPI()


cursos = {
    1: {"titulo": "Inicial", "aulas": 112, "horas": 58},
    2: {"titulo": "Segundo", "aulas": 100, "horas": 20},
}


@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{id}")
async def get_curso(
    id: int = Path(
        title="Id do curso",
        description="valor de 1 a 2",
        gt=0,
        lt=3,
    )
):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado",
        )


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1
    cursos[next_id] = curso
    return curso


@app.put("/cursos/{id}")
async def put_curso(id: int, curso: Curso):
    if id in cursos.keys():
        cursos[id] = curso
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe esse curso",
        )


@app.delete("/cursos/{id}")
async def delete_curso(id: int):
    if id in cursos.keys():
        cursos.pop(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
