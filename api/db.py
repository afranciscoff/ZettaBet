# api/db.py  23-01-2026 (alinhado com DDL real)
import logging
from sqlalchemy import (
    create_engine, Column, Integer, BigInteger, SmallInteger,
    String, Numeric, DateTime, ARRAY
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = (
    "postgresql://neondb_owner:npg_Lqjh6vGBVi5r@"
    "ep-black-hill-acpnaibc-pooler.sa-east-1.aws.neon.tech/"
    "Faixabs?sslmode=require"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


class ExternalPalpite(Base):
    __tablename__ = "external_palpite"

    id = Column(BigInteger, primary_key=True)
    loteria_id = Column(SmallInteger, nullable=False)
    dezenas = Column(ARRAY(Integer), nullable=False)
    qtd_dezenas = Column(SmallInteger, nullable=False)
    motor_nome = Column(String(100), nullable=False)
    motor_versao = Column(String(50))
    origem = Column(String(50), default="externo")
    concurso_ref = Column(Integer)
    seed = Column(BigInteger)
    score_interno = Column(Numeric(6, 4))
    meta_json = Column(JSONB)           # ✅ livre
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------- função auxiliar ----------
def busca_loteria_id(session, codigo: str = "lotofacil") -> int:
    """Devolve o id numérico da loteria pelo código."""
    # Ajuste a query conforme sua tabela real
    # Exemplo fixo para Lotofácil
    return 1   # <-- substitua por SELECT real quando tiver tabela loteria


def insere_palpite(
    dezenas: list[int],
    motor_nome: str,
    motor_versao: str | None = None,
    origem: str = "externo",
    concurso_ref: int | None = None,
    seed: int | None = None,
    score_interno: float | None = None,
    metadata: dict | None = None
) -> int:
    """Insere 1 palpite externo e devolve o id."""
    with SessionLocal() as session:
        palpite = ExternalPalpite(
            loteria_id=busca_loteria_id(session),  # SMALLINT obrigatório
            dezenas=dezenas,
            qtd_dezenas=len(dezenas),
            motor_nome=motor_nome,
            motor_versao=motor_versao,
            origem=origem,
            concurso_ref=concurso_ref,
            seed=seed,
            score_interno=score_interno,
            metadata=metadata or {}
        )
        try:
            session.add(palpite)
            session.commit()
            logger.info("Palpite inserido id=%s", palpite.id)
            return palpite.id
        except Exception as e:
            logger.exception("Insert falhou: %s", e)
            session.rollback()
            raise


