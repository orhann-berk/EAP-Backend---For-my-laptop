from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Example:
# postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = "postgresql://orhannberk:postgres@localhost:5432/eap"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
