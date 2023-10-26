from fastapi import FastAPI

from controllers import artigo_controler, usuario_controller

app = FastAPI(
    title="Api Usuário e artigos",
    version="0.0.1",
    description="Uma api para aprender fastapi",
)

app.include_router(usuario_controller.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(artigo_controler.router, prefix="/artigos", tags=["artigos"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
