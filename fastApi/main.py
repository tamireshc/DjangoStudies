from typing import List

from fastapi import FastAPI, Header, HTTPException, Path, Response, status

from models import Curso, cursos

app = FastAPI(
    title="Api Cursos",
    version="0.0.1",
    description="Uma api para aprender fastapi",
)


@app.get(
    "/cursos",
    description="Exibe todos os cursos cadastrados",
    summary="Retorna todos os cursos",
    response_model=List[Curso],
)
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
        curso = cursos[id - 1]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado",
        )


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    cursos.append(curso)
    return curso


@app.put("/cursos/{id}")
async def put_curso(id: int, curso: Curso):
    for curso in cursos:
        if id == curso.id:
            index = cursos.index(curso)
            print("index", index)
            cursos[1] = curso
            return cursos[1]
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


@app.get("/calculadora")
async def calculadora(
    a: int,
    b: int,
    c: int,
    x: str = Header(
        default=None,
    ),
):
    result = a + b + c
    print(x)
    return {"soma": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
