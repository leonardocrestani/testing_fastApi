from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .repository import PedidoRepository

router = APIRouter()

# Cria uma instância do repositório de pedidos para chamar as fuções
pedido_repository = PedidoRepository()

class Pedido(BaseModel):
    item: str
    quantidade: int

class AtualizarPedido(BaseModel):
    quantidade: int

@router.get("")
async def buscar_pedidos():
    # Busca a lista de todos os pedidos do repositório
    pedidos = pedido_repository.buscar_pedidos()
    return {"Pedidos": pedidos}

@router.get("/concluidos")
async def buscar_pedidos_concluidos():
    # Busca a lista de todos os pedidos do repositório
    pedidos = pedido_repository.buscar_pedidos()
    concluidos = []
    # Filtra os pedidos concluídos
    for pedido in pedidos:
        if pedido["status"] == "Concluido":
            concluidos.append(pedido)
    return {"Pedidos Concluídos": concluidos}

@router.get("/{pedido_id}")
async def buscar_pedido(pedido_id: int):
    # Busca a lista de todos os pedidos do repositório
    pedidos = pedido_repository.buscar_pedidos()
    pedido = None
    # Procura o pedido pelo ID
    for p in pedidos:
        if p["id"] == pedido_id:
            pedido = p
            break
    if pedido:
        return pedido
    else:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.post("/adicionar_pedido", status_code=201)
async def adicionar_pedido(pedido: Pedido):
    # Verifica se a quantidade é válida
    if pedido.quantidade <= 0:
        raise HTTPException(status_code=400, detail="A quantidade deve ser maior que zero")  
    # Cria um novo pedido com um ID único que vai ser o ID seguinte do ultimo e adiciona ao array de objetos dos pedidos utilizando a função do repositorio
    novo_pedido = {"id": len(pedido_repository.buscar_pedidos()) + 1, "item": pedido.item, "quantidade": pedido.quantidade, "status": "Em andamento"}
    pedido_repository.adicionar_pedido(novo_pedido)
    return {"message": "Pedido adicionado com sucesso", "pedido": novo_pedido}

@router.put("/atualizar_pedido/{pedido_id}", status_code=204)
async def atualizar_pedido(pedido_id: int, pedido: AtualizarPedido):
    # Verifica se a quantidade é válida
    if pedido.quantidade <= 0:
        raise HTTPException(status_code=400, detail="A quantidade deve ser maior que zero")
    # Busca a lista de todos os pedidos do repositório
    pedidos = pedido_repository.buscar_pedidos()
    pedido_atual = None
    # Procura o pedido pelo ID
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            pedido_atual = pedido
            break
    if pedido_atual:
        # Se pedido existir verifica se o pedido pode ser atualizado com base no status (se status for não iniciado apenas pode ser atualizado)
        if pedido_atual["status"] in ["Concluido", "Em andamento"]:
            raise HTTPException(status_code=400, detail=f"Não é possível atualizar pedidos {pedido_atual['status']}")
        # Atualiza a quantidade do pedido com base no ID, vai atualizar o objeto que esta no repositório
        pedido_repository.atualizar_pedido(pedido_id, {"item": pedido_atual["item"], "quantidade": pedido["quantidade"]})
        return
    else:
        # Retorna 404 (NOT FOUND) se o pedido não for encontrado
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.put("/concluir_pedido/{pedido_id}", status_code=204)
async def concluir_pedido(pedido_id: int):
    # Tenta concluir o pedido no repositório se for concluido recebe TRUE e devolve a mensagem
    # Troca o status do pedido no objeto dentro do repositório para Concluido
    pedido_atualizado = pedido_repository.concluir_pedido(pedido_id)
    if pedido_atualizado:
        return
    else:
        # Retorna 404 (NOT FOUND) se o pedido não for encontrado
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

@router.delete("/remover_pedido/{pedido_id}", status_code=204)
async def remover_pedido(pedido_id: int):
    # Tenta remover o pedido no repositório se for removido recebe TRUE e devolve a mensagem
    # Retira o pedido do array dos pedidos
    removido = pedido_repository.remover_pedido(pedido_id)
    if removido:
        return
    else:
         # Retorna 404 (NOT FOUND) se o pedido não for encontrado
         raise HTTPException(status_code=404, detail="Pedido não encontrado")
