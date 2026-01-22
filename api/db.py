# api/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (                      # mesma pasta ou ajuste o import
    Loteria, ExternalPalpite, Base
)
DATABASE_URL=postgresql://neondb_owner:npg_Lqjh6vGBVi5r@ep-black-hill-acpnaibc-pooler.sa-east-1.aws.neon.tech/Faixabs?sslmode=require&channel_binding=require

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def inserir_palpite_lotofacil(
    dezenas: list[int],
    motor_nome: str,
    motor_versao: str | None = None,
    seed: int | None = None,
    metadata: dict | None = None
) -> int:
    with SessionLocal() as session:
        loteria = (
            session.query(Loteria)
            .filter_by(codigo="lotofacil", ativa=True)
            .one()
        )

        palpite = ExternalPalpite(
            loteria_id=loteria.id,
            dezenas=dezenas,
            qtd_dezenas=len(dezenas),
            motor_nome=motor_nome,
            motor_versao=motor_versao,
            seed=seed,
            metadata=metadata
        )
        try:
            session.add(palpite)
            session.commit()
            return palpite.id
        except (IntegrityError, DataError):
            session.rollback()
            raise