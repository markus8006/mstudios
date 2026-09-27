from datetime import datetime

from sqlalchemy import JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Funcionario:
    __tablename__ = 'funcionarios'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class Agendamento:
    __tablename__ = 'agendamentos'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data: Mapped[datetime]
    horario_inicio: Mapped[datetime]
    cortes: Mapped[list[str]] = mapped_column(JSON)
    tempo_total: Mapped[float]
    nome_cliente: Mapped[str]
    id_funcionario: Mapped[int] = mapped_column(ForeignKey(Funcionario.id))
    telefone_cliente: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    aceito: Mapped[int]
