from datetime import datetime
from http import HTTPStatus

from mstudios.models import Agendamento
from mstudios.schemas import AgendamentoBase, AgendamentoPublic


def test_retorno_cafe(client):
    response = client.get('/quero_cafe')

    assert response.status_code == HTTPStatus.IM_A_TEAPOT
    assert response.json() == {'message': 'NO, IM A TEAPOT'}


def test_criar_agendamento(client, agendamento_base, mock_db_time):

    with mock_db_time(model=Agendamento):
        resposta = AgendamentoPublic(
            **agendamento_base.model_dump(),
            id=1,
            aceito=0,
            tempo_total=60.0,
        )

    response = client.post(
        '/agendamento', json=agendamento_base.model_dump(mode='json')
    )

    assert response.json() == resposta.model_dump(mode='json')
    assert response.status_code == HTTPStatus.CREATED


def test_read_agendamentos(client):
    response = client.get('/agendamento')

    assert response.json() == {'agendamentos': []}
    assert response.status_code == HTTPStatus.OK


def test_read_agendamento_with_data(client, mock_db_time, agendamento_base):

    with mock_db_time(model=Agendamento):
        resposta = AgendamentoPublic(
            **agendamento_base.model_dump(),
            id=1,
            aceito=0,
            tempo_total=60.0,
        )

    client.post('/agendamento', json=agendamento_base.model_dump(mode='json'))

    response = client.get('/agendamento')

    assert response.json() == {
        'agendamentos': [resposta.model_dump(mode='json')]
    }
    assert response.status_code == HTTPStatus.OK


def test_read_agendamento_with_id(client, mock_db_time, agendamento_base):

    agendamento_id = 1
    with mock_db_time(model=Agendamento):
        resposta = AgendamentoPublic(
            **agendamento_base.model_dump(),
            id=1,
            aceito=0,
            tempo_total=60.0,
        )

    client.post('/agendamento', json=agendamento_base.model_dump(mode='json'))

    response = client.get(f'/agendamento/{agendamento_id}')

    assert response.json() == resposta.model_dump(mode='json')
    assert response.status_code == HTTPStatus.OK


def test_read_agendamento_not_found(client):
    response = client.get(f'agendamento/{1}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Agendamento not found'}


def test_update_agendamento(client, mock_db_time, agendamento_base):

    agendamento_id = 1
    with mock_db_time(model=Agendamento):
        Novo_agendamento = AgendamentoBase(
            data=datetime(2026, 12, 1),
            horario_inicio=datetime(2026, 12, 1),
            cortes=['corte1'],
            nome_cliente='Monica',
            id_funcionario=1,
            telefone_cliente='9999-8888',
        )
        agendamento_atualizado = AgendamentoPublic(
            **Novo_agendamento.model_dump(), id=1, tempo_total=60.0, aceito=0
        )

    client.post('/agendamento', json=agendamento_base.model_dump(mode='json'))

    response_put = client.put(
        f'/agendamento/{agendamento_id}',
        json=Novo_agendamento.model_dump(mode='json'),
    )

    assert response_put.json() == agendamento_atualizado.model_dump(
        mode='json'
    )
    assert response_put.status_code == HTTPStatus.OK

    response_get = client.get(f'/agendamento/{agendamento_id}')

    assert response_get.json() == agendamento_atualizado.model_dump(
        mode='json'
    )
    assert response_get.status_code == HTTPStatus.OK


def test_delete_agendamento(client, agendamento_base):

    client.post('/agendamento', json=agendamento_base.model_dump(mode='json'))

    client.delete(f'/agendamento/{1}')

    response = client.get('/agendamento')

    assert response.json() == {'agendamentos': []}
    assert response.status_code == HTTPStatus.OK


def test_delete_nothing(client):

    response = client.delete(f'/agendamento/{1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Agendamento not found'}
