from fastapi import FastAPI
from fastapi.routing import APIRouter
from pedidos.pedidos import router as pedidos_router

app = FastAPI()

# Cria um roteador para incluir os modulos roteadores
router = APIRouter()

# Inclui as rotas do modulo de pedidos
router.include_router(pedidos_router, prefix="/pedidos", tags=["pedidos"])

app.include_router(router)