from datetime import datetime

from pydantic import BaseModel


class AgendamentoBase(BaseModel):
    data: datetime
    horario_inicio: datetime
    cortes: list[str]
    nome_cliente: str
    id_funcionario: int
    telefone_cliente: str


class AgendamentoPublic(AgendamentoBase):
    tempo_total: float
    aceito: int
    id: int


class AgendamentoDB(AgendamentoPublic):
    created_at: datetime


class Funcionario(BaseModel):
    id: int
    nome: str


class AgendamentoPublicList(BaseModel):
    users: list[AgendamentoPublic]
