import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from fastapi.testclient import TestClient

from core.authentication.hashing import hash_password
from core.database.connection import get_db
from core.database.orm import Base
from main import app
from users.models import User


@pytest.fixture(scope="session")
def test_db():
    test_db_url = "mysql+pymysql://root:ozcoding@127.0.0.1:33060/test"
    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)  # test db table 생성
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    connection = test_db.connect()

    connection.begin()
    session = sessionmaker()(bind=connection)

    yield session

    session.rollback()
    connection.close()


@pytest.fixture
def client(test_session):
    def test_get_db():
        yield test_session

    app.dependency_overrides[get_db] = test_get_db
    return TestClient(app=app)


@pytest.fixture(scope="function")
def test_user(test_session):
    new_password = hash_password(plain_text="test-pw")
    new_user = User.create(username="test", password=new_password)
    test_session.add(new_user)
    test_session.commit()
    return new_user
