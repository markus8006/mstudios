from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from mstudios.models import Agendamento
from mstudios.schemas import AgendamentoBase, AgendamentoDB


def test_db_new_agendamento(session, mock_db_time):
    data = datetime.now()
    with mock_db_time(model=Agendamento) as time:
        novo_agendamento = AgendamentoBase(
            data=data,
            horario_inicio=data,
            cortes=['corte1', 'corte2'],
            nome_cliente='Alice',
            id_funcionario=1,
            telefone_cliente='9999-9999',
        )
        agendamento_db = Agendamento(
            **novo_agendamento.model_dump(), tempo_total=60.0, aceito=0
        )

        resposta = AgendamentoDB(
            **novo_agendamento.model_dump(),
            created_at=time,
            id=1,
            tempo_total=60.0,
            aceito=0,
        )

        session.add(agendamento_db)
        session.commit()

        agendamento = session.scalar(
            select(Agendamento).where(Agendamento.nome_cliente == 'Alice')
        )

        assert asdict(agendamento) == resposta.model_dump()
