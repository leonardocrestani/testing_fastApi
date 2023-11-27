from unittest.mock import MagicMock

# Arquivo para armazenar os mocks criados
mock_pedidos = MagicMock()
mock_pedidos.return_value = [
    {"id": 1, "item": "Mock Pizza", "quantidade": 2, "status": "Em andamento"},
    {"id": 2, "item": "Mock Hambúrguer", "quantidade": 1, "status": "Concluido"},
    {"id": 3, "item": "Mock Hambúrguer", "quantidade": 1, "status": "Nao iniciado"},
]

mock_pedidos_concluidos = MagicMock()
mock_pedidos_concluidos.return_value = [
  {"id": 2, "item": "Mock Hambúrguer", "quantidade": 1, "status": "Concluido"}
]