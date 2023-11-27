class PedidoRepository:
    # Lista de pedidos para simular um banco de dados
    pedidos = [
        {"id": 1, "item": "Pizza", "quantidade": 2, "status": "Em andamento"},
        {"id": 2, "item": "Hambúrguer", "quantidade": 1, "status": "Concluido"},
        {"id": 3, "item": "Salada", "quantidade": 3, "status": "Em andamento"},
        {"id": 4, "item": "Sushi", "quantidade": 2, "status": "Nao inciado"},
        {"id": 5, "item": "Lasanha", "quantidade": 1, "status": "Concluido"},
        {"id": 6, "item": "Sorvete", "quantidade": 2, "status": "Em andamento"},
        {"id": 7, "item": "Frango Grelhado", "quantidade": 1, "status": "Nao iniciado"},
    ]

    # O @classmethod é utilizado para indicar que o método pertence a classe
    # Isso significa que eles podem ser chamados direto na classe
    # A utilização é feita pois essa é uma classe global de repositório
    # O uso do cls é feito para referenciar a propria classe e conseguir chamar o objeto que simula o banco
    @classmethod
    def buscar_pedidos(cls):
        return cls.pedidos

    @classmethod
    def adicionar_pedido(cls, novo_pedido):
        cls.pedidos.append(novo_pedido)

    @classmethod
    def atualizar_pedido(cls, pedido_id, novo_pedido):
        for p in cls.pedidos:
            if p["id"] == pedido_id:
                p.update(novo_pedido)
                return

    @classmethod
    def concluir_pedido(cls, pedido_id):
        for pedido in cls.pedidos:
            if pedido["id"] == pedido_id:
                pedido["status"] = "Concluido"
                return True
        return False

    @classmethod
    def remover_pedido(cls, pedido_id):
        for pedido in cls.pedidos:
            if pedido["id"] == pedido_id:
                cls.pedidos.remove(pedido)
                return True
        return False
