from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from mstudios.schemas import (
    AgendamentoBase,
    AgendamentoDB,
    AgendamentoPublic,
    AgendamentoPublicList,
)

app = FastAPI()

database = []


@app.get('/quero_cafe', status_code=HTTPStatus.IM_A_TEAPOT)
def get_coffe():
    return {'message': 'NO, IM A TEAPOT'}


@app.post(
    '/agendamento',
    response_model=AgendamentoPublic,
    status_code=HTTPStatus.CREATED,
)
def create_agendamento(agendamento: AgendamentoBase):
    novo_agendamento = AgendamentoDB(
        **agendamento.model_dump(mode='json'),
        id=1,
        aceito=0,
        tempo_total=60.0,
        created_at=datetime(2026, 1, 12),
    )
    database.append(novo_agendamento)
    return novo_agendamento


@app.get(
    '/agendamento',
    status_code=HTTPStatus.OK,
    response_model=AgendamentoPublicList,
)
def read_agendamento():
    return {'users': database}


@app.put('agendamento/{agendamento_id}', response_model=AgendamentoPublic)
def update_agendamento(agendamento_id : int, novo_agendamento : AgendamentoBase):
    if agendamento_id < 1 or agendamento_id > database(len):
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail="agendamento not found" 
        )

    agendamento = database[agendamento_id - 1]
    novo_agendamento = agendamento
    
