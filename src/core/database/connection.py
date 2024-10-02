from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.database_url)
SessionFactory = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
