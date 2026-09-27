from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from mstudios.database import get_session
from mstudios.models import Agendamento
from mstudios.schemas import (
    AgendamentoBase,
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
def create_agendamento(
    agendamento: AgendamentoBase, session: Session = Depends(get_session)
):

    agendamento_db = Agendamento(
        **agendamento.model_dump(), aceito=0, tempo_total=60.0
    )
    session.add(agendamento_db)
    session.commit()
    session.refresh(agendamento_db)
    return agendamento_db


@app.get(
    '/agendamento',
    status_code=HTTPStatus.OK,
    response_model=AgendamentoPublicList,
)
def read_agendamento(
    offset=0, limit=100, session: Session = Depends(get_session)
):
    agendamentos = session.scalars(
        select(Agendamento).offset(offset).limit(limit)
    ).all()
    return {'agendamentos': agendamentos}


@app.get(
    '/agendamento/{agendamento_id}',
    status_code=HTTPStatus.OK,
    response_model=AgendamentoPublic,
)
def read_agendamento_id(
    agendamento_id: int, session: Session = Depends(get_session)
):
    agendamento_db = session.scalar(
        select(Agendamento).where(Agendamento.id == agendamento_id)
    )
    if not agendamento_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Agendamento not found'
        )

    return agendamento_db


@app.put(
    '/agendamento/{agendamento_id}',
    status_code=HTTPStatus.OK,
    response_model=AgendamentoPublic,
)
def update_agendamento(
    agendamento_id: int,
    novo_agendamento: AgendamentoBase,
    session: Session = Depends(get_session),
):

    agendamento_db = session.scalar(
        select(Agendamento).where(Agendamento.id == agendamento_id)
    )
    if not agendamento_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Agendamento not found'
        )

    if agendamento_db.aceito != 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail='Placeholder',
        )

    agendamento_atualizado = novo_agendamento.model_dump()

    for chave, valor in agendamento_atualizado.items():
        setattr(agendamento_db, chave, valor)

    session.commit()
    session.refresh(agendamento_db)

    return agendamento_db


@app.delete(
    '/agendamento/{agendamento_id}',
    status_code=HTTPStatus.OK,
    response_model=AgendamentoPublic,
)
def delete_agendamento(
    agendamento_id: int,
    session: Session = Depends(get_session),
):
    agendamento_db = session.scalar(
        select(Agendamento).where(Agendamento.id == agendamento_id)
    )
    if not agendamento_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Agendamento not found'
        )

    session.delete(agendamento_db)
    session.commit()

    return agendamento_db
