from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AgendamentoBase(BaseSchemas):
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


class Funcionario(BaseSchemas):
    id: int
    nome: str


class AgendamentoPublicList(BaseSchemas):
    agendamentos: list[AgendamentoPublic]
