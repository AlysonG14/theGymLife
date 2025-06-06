import uuid
from enum import Enum # Essa função ela vai definir uma ação para escolher qual
from fastapi import APIRouter, File, UploadFile, Form, Query
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Optional


router = APIRouter(prefix="/biblioteca_de_livros")
IMAGEDIR = "static/images" # Esse vai ser o diretório onde colocamos a imagem do local

# Permite que vai criar uma simulação de Banco de Dados em memória (simulado)
livro_db = [

    {
        "id": 1,
        "titulo": "A Revolução dos Bichos",
        "autor": "George Orwell",
        "descricao": "Escrita em plena Segunda Guerra Mundial e publicada em 1945 depois de ter sido rejeitada por várias editoras, essa pequena narrativa causou desconforto ao satirizar ferozmente a ditadura stalinista numa época em que os soviéticos ainda eram aliados do Ocidente na luta contra o eixo nazifascista.",
        "ano_publicacao": 1945,
        "paginas": 152,
        "valor": 16.68,
        "genero": "FICCAO_CIENTIFICA",
    },
    {
        "id": 2,
        "titulo": "1984",
        "autor": "George Orwell",
        "descricao": "É um romance distópico que explora um futuro totalitário onde a privacidade é inexistente e a liberdade é um sonho distante. Ele mostra uma sociedade controlada pelo Estado, onde o Grande Irmão vigia constantemente os cidadãos e a verdade é manipulada para servir à ideologia do Partido. ",
        "ano_publicacao": 1949,
        "paginas": 336,
        "valor": 18.00,
        "genero": "FICCAO_CIENTIFICA",
    }
]


class GeneroLivro(str, Enum):
    SUSPENSE = 'SUSPENSE'
    DESENVOLVIMENTO = 'DESENVOLVIMENTO PESSOAL'
    TERROR = 'TERROR'
    FICCAO_CIENTIFICA = 'FICÇÃO CIENTÍFICA'
    FINANCAS = 'FINANÇAS'
    ROMANCE = 'ROMANCE'
    LITERATURA = 'LITERATURA'
    RELIGIAO = 'RELIGIÃO'


class BibliotecadeLivrosResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    descricao: str
    ano_publicacao: int
    paginas: int
    valor: float
    genero: GeneroLivro

class BibliotecadeLivrosRequest(BaseModel):
    id: int
    titulo: str
    autor: str
    descricao: str
    ano_publicacao: int
    paginas: int
    valor: float
    genero: GeneroLivro

# Rota GET -> Para listar livros

@router.get("/biblioteca/livros/")
async def listar_livro(
    id: Optional[int] = Query(None),
    titulo: Optional[str] = Query(None)
):
    if id is not None and not isinstance(id, int):
        return {"detail": "ID deve ser um número inteiro válido."}
    
    resultados = livro_db
    
    if id is not None:
        resultados = [livro for livro in resultados if livro["id"] == id]
    
    if titulo:
        resultados = [livro for livro in resultados if titulo.lower() in livro["titulo"].lower()]

    if not resultados:
        return {"mensagem": "Nenhum livro encontrado."}
    
    return {"livros": resultados}

# Rota GET -> Para pegar o livro em ID

@router.get("/biblioteca/livros/{livro_id}", response_model=BibliotecadeLivrosResponse)
async def buscar_livro_id(livro_id: int):
    for livro in livro_db:
        if livro['id'] == livro_id:
            return livro
    return {"Erro:" "Livro não encontrado"}

# Rota POST -> para criar livros

@router.post("/biblioteca/criar/", response_model=BibliotecadeLivrosResponse, status_code=201)
async def criar_livro(id: int = Form(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    descricao: str = Form(...),
    ano_publicacao: int = Form(...),
    paginas: int = Form(...),
    valor: float = Form(...),
    genero: GeneroLivro = Form(...),
    imagem: UploadFile = File(...)
    ):

    # Salva imagem no diretório
    filename = f"{uuid.uuid4()}.jpg"
    contents = await imagem.read()

    # Salvar o Arquivo
    with open(f"{IMAGEDIR}{filename}", "wb") as f:
        f.write(contents)

        livro_data = {
            "id": id,
            "titulo": titulo,
            "autor": autor,
            "descricao": descricao,
            "ano_publicacao": ano_publicacao,
            "paginas": paginas,
            "valor": valor,
            "genero": genero,
            "imagem": filename 
            
        }

        livro_db.append(livro_data)
        return livro_data

# Rota PATCH -> Para atualizar o Livro

@router.patch('/biblioteca/atualizar/{livro_id}', response_model=BibliotecadeLivrosResponse)
async def atualizar_livro(livro_id: int, livro_atualizado: BibliotecadeLivrosRequest):
    for i, livro in enumerate(livro_db):
        if livro['id'] == livro_id:
            livro_db[i] = livro_atualizado.dict()
            return livro_db[i]
    return {'Erro': "Livro não Encontrado"}

# Rota DELETE -> Para deletar o Livro

@router.delete('/biblioteca/delete/{livro_id}', status_code=201)
async def delete_livro(livro_id: int):
    for i, livro in enumerate (livro_db):
        if livro['id'] == livro_id:
            return livro_db.pop(i)
    return {"Erro": "Livro não Encontrado"}
        
