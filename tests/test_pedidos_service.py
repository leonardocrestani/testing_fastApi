from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from mocks.pedidos_mock import mock_pedidos, mock_pedidos_concluidos
from main import app

client = TestClient(app)

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
def test_buscar_pedidos():
    # Testa a rota de buscar todos pedidos
    response = client.get("/pedidos")
    # Verifica status code se é 200 status de sucesso ao buscar
    assert response.status_code == 200
    # Verifica se o JSON de resposta corresponde ao mock de pedidos utilizado
    assert response.json() == {"Pedidos": mock_pedidos.return_value}

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
def test_buscar_pedidos_concluidos():
    # Testa a rota de busca de pedidos concluídos
    response = client.get("/pedidos/concluidos")
    # Verifica status code se é 200 status de sucesso ao buscar
    assert response.status_code == 200
    # Verifica se o JSON de resposta corresponde aos pedidos concluídos no mock
    # O mock utilizado é diferente nele só consta o unico pedido concluido do objeto principal
    # Se o serviço de pedidos funcionar corretamente deve devolver somente o unico pedido concluido e assim a assert estando correta
    assert response.json() == {"Pedidos Concluídos": mock_pedidos_concluidos.return_value}

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
def test_buscar_pedido():
    # Testa a rota de busca de um pedido específico
    response = client.get("/pedidos/1")
    # Verifica status code se é 200 status de sucesso ao buscar
    assert response.status_code == 200
    # Verifica se o ID do pedido recebido ao enviado pelos parametros
    assert response.json()["id"] == 1

    # Teste caso de erro enviando um ID inexistente
    response = client.get("/pedidos/20")
    # Verifica status code se é 404 status de not found (nao encontrado)
    assert response.status_code == 404
    # Verifica se a mensagem corresponde a mensagem esperada
    assert response.json()["detail"] == "Pedido não encontrado"

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
@patch('pedidos.repository.PedidoRepository.adicionar_pedido', MagicMock().return_value({}))
def test_adicionar_pedido():
    # Testa a rota de adição de um novo pedido
    novo_pedido = {"item": "Batata Frita", "quantidade": 2}
    response = client.post("/pedidos/adicionar_pedido", json=novo_pedido)
    # Verifica status code se é 201 status de criado
    assert response.status_code == 201
    # Verifica se a mensagem de sucesso e o ID do novo pedido correspondem e foi criado corretamente
    assert response.json()["message"] == "Pedido adicionado com sucesso"
    assert 4 == response.json()["pedido"]["id"]

    # Teste caso de erro enviando uma quantidade de itens do pedido como 0 (erro o pedido deve ter quantidade maior)
    novo_pedido = {"item": "Batata Frita", "quantidade": 0}
    response = client.post("/pedidos/adicionar_pedido", json=novo_pedido)
    # Verifica se a mensagem corresponde a mensagem de erro esperada
    # A mensagem vem no objeto detail do HttpException por isso é pega desta variavel (EX: como se fosse detalhes do erro)
    assert response.json()["detail"] == "A quantidade deve ser maior que zero"
    # Verifica status code se é 400 status de bad request (requisição mal formada os valores estao incorretos)
    assert response.status_code == 400

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
@patch('pedidos.repository.PedidoRepository.atualizar_pedido', MagicMock().return_value({}))
def test_atualizar_pedido():
    # Testa a rota de atualizar um pedido
    pedido_atualizado = {"quantidade": 3}
    response = client.put("/pedidos/atualizar_pedido/3", json=pedido_atualizado)
    # Verifica status code se é 204 status de no content mas que o pedido foi alterado com sucesso
    assert response.status_code == 204

    # Teste caso de erro tentando atualizar o pedido para uma quantidade de itens do pedido como 0 (erro o pedido deve ter quantidade maior)
    pedido_atualizado = {"quantidade": 0}
    response = client.put("/pedidos/atualizar_pedido/1", json=pedido_atualizado)
    print(response.json())
    # Verifica status code se é 400 status de bad request (requisição mal formada os valores estao incorretos)
    assert response.status_code == 400
    # Verifica se a mensagem de erro esta correta
    assert response.json()["detail"] == "A quantidade deve ser maior que zero"

    # Teste caso de erro passando ID inexistente para pedido
    pedido_atualizado = {"quantidade": 2}
    response = client.put("/pedidos/atualizar_pedido/50", json=pedido_atualizado)
    # Verifica status code se é 404 status de not found (nao encontrado)
    assert response.status_code == 404
    # Verifica se a mensagem de erro esta correta
    assert response.json()["detail"] == "Pedido não encontrado"

    # Teste caso de erro passando tentando atualizar um pedido que esta em andamento ou que ja foi concluido
    pedido_atualizado = {"quantidade": 2}
    response = client.put("/pedidos/atualizar_pedido/1", json=pedido_atualizado)
    # Verifica status code se é 400 status de bad request (requisição tenta alterar um recurso de forma incorreta)
    assert response.status_code == 400
    # Verifica se a mensagem de erro esta correta
    assert response.json()["detail"] == "Não é possível atualizar pedidos Em andamento"

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
@patch('pedidos.repository.PedidoRepository.concluir_pedido', MagicMock(return_value=True))
def test_concluir_pedido():
    # Testa a rota de concluir pedido
    response = client.put("/pedidos/concluir_pedido/1")
    # Verifica status code se é 204 status de no content mas que o pedido foi alterado com sucesso
    assert response.status_code == 204

    # Teste caso de erro ao tentar atualizar um pedido que não existe
    # E necessario criar um nova função porque ela é específica para testar os cenários de erro dessa rota
    # Neste caso para este teste o decorator altera o mock da funcao concluir pedido simulando que ocorreu um erro
    @patch('pedidos.repository.PedidoRepository.concluir_pedido', MagicMock(return_value=False))
    def test_concluir_pedido_erro():
        response = client.put("/pedidos/concluir_pedido/20")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pedido não encontrado"

    # A função interna deve ser chamada para rodar o método criado e o teste que utiliza decorators aninhados.
    test_concluir_pedido_erro()

@patch('pedidos.repository.PedidoRepository.buscar_pedidos', mock_pedidos)
@patch('pedidos.repository.PedidoRepository.remover_pedido', MagicMock(return_value=True))
def test_remover_pedido():
    # Testa a rota de remover pedido
    response = client.delete("/pedidos/remover_pedido/3")
    # Verifica status code se é 204 status de no content mas que o pedido foi removido com sucesso (nao possui body pois foi removido)
    # O body do objeto removido não precisa ser testado somente o status para saber se ocorreu de forma correta a remoção
    assert response.status_code == 204

    # Teste caso de erro ao tentar atualizar um pedido que não existe
    # E necessario criar um nova função porque ela é específica para testar os cenários de erro dessa rota
    @patch('pedidos.repository.PedidoRepository.remover_pedido', MagicMock(return_value=False))
    def test_remover_pedido_erro():
        response = client.delete("/pedidos/remover_pedido/15")
        assert response.status_code == 404
        assert response.json()["detail"] == "Pedido não encontrado"

    # A função interna deve ser chamada para rodar o método criado e o teste que utiliza decorators aninhados.
    test_remover_pedido_erro()
