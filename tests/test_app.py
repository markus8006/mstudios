from http import HTTPStatus

from mstudios.models import Agendamento
from mstudios.schemas import AgendamentoPublic


def test_retorno_cafe(client):
    response = client.get('/quero_cafe')

    assert response.status_code == HTTPStatus.IM_A_TEAPOT
    assert response.json() == {'message': 'NO, IM A TEAPOT'}


def test_criar_agendamento_sem_db(client, agendamento_base, mock_db_time):

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


def test_read_agendamento(client, agendamento_base, mock_db_time):
    response = client.get('/agendamento')

    with mock_db_time(model=Agendamento):
        resposta = AgendamentoPublic(
            **agendamento_base.model_dump(),
            id=1,
            aceito=0,
            tempo_total=60.0,
        )
        breakpoint()

    assert response.json() == {'users': [resposta.model_dump(mode='json')]}
    assert response.status_code == HTTPStatus.OK
