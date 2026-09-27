from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from mstudios.app import app
from mstudios.models import table_registry
from mstudios.schemas import AgendamentoBase, Funcionario


@pytest.fixture
def date_fot_test():
    return datetime(2026, 12, 1)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 12, 1)):

    def _fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', _fake_time_hook)

    yield time

    event.remove(model, 'before_insert', _fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def melissa():
    return Funcionario(id=1, nome='Melissa')


@pytest.fixture
def agendamento_base():
    novo_agendamento = AgendamentoBase(
        data=datetime(2026, 12, 1),
        horario_inicio=datetime(2026, 12, 1),
        cortes=['corte1', 'corte2'],
        nome_cliente='Alice',
        id_funcionario=1,
        telefone_cliente='9999-9999',
    )
    return novo_agendamento
