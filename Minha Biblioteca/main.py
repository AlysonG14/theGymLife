import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import biblioteca_de_livros_router.biblioteca_de_livros
from fastapi.templating import Jinja2Templates
from typing import Optional
from biblioteca_de_livros_router.biblioteca_de_livros import livro_db

app = FastAPI(title='Book Lover', version="1.0.0", description='Seja-Bem vindo ao uma coleção de biblioteca que criamos')

app.include_router(biblioteca_de_livros_router.biblioteca_de_livros.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')


# Função assíncrona: permite que a requisição não bloqueie o servidor enquanto outras tarefas são executadas
@app.get("/")
async def renderizar_pagina01(request: Request):
    return templates.TemplateResponse("homepage.html", {
        "request": request,
        "title": "Book Lover",
        "sub_title": "Welcome to my library collection books",
    })

# Agora, vamos criar uma template onde possa ser rendealizado usando a requsição GET para listar todos os livros armazenados do banco de dados simulado
@app.get("/page/booklover.com", response_class=HTMLResponse)
async def listar_livros(request: Request, titulo: Optional[str] = None, id: Optional[int] = None):
    result = livro_db
    if id:
        result = [livro for livro in livro_db if livro['id'] == id]
    elif titulo:
        result = [livro for livro in livro_db if titulo.lower() in livro['titulo'].lower()]

    return templates.TemplateResponse("home.html", {
        "request": request,
        "title": "Book Lover",
        "search_bar" : "What do you want?",
        "username01": "Login",
        "username02": "Password",
        "nav01": "About a Company",
        "nav02": "Our Store",
        "nav03": "Our App",
        "livros": result
    })

@app.get("/page/booklover.com/{pk}", response_class=HTMLResponse)
async def descricao(request: Request, pk: int):
    for livro in livro_db:
        if livro['id'] == pk:
            return templates.TemplateResponse("page_book.html", {
                "request": request,
                "livro": livro,
                "descrição": "Descrição do Livro"
    })
    return HTMLResponse(content="Livro não encontrado", status_code=204)

@app.get("/goodbye")
async def goodbye():
    return {"Thank you": "Come back later, goodbye! 😎😎"}

if __name__ == "__main__":  
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
