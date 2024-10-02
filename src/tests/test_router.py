from core.authentication.hashing import check_password, hash_password
from core.authentication.jwt import _decode_access_token, create_access_token, JWTService
from users.models import User

from schema import Schema


def test_root(client):
    # given

    # when
    response = client.get("/")

    # then
    assert response.status_code == 200
    assert Schema({"Hello": "World"}).validate(response.json())


def test_sign_up_201(client, test_session):
    # given

    # when
    response = client.post(
        "/users/sign-up",
        json={"username": "test", "password": "test-pw"}
    )

    # then
    assert response.status_code == 201
    assert Schema(
        {
            "id": int,
            "username": "test",
            "created_at": str,
        }
    ).validate(response.json())

    user = test_session.query(User).filter(User.username == "test").first()
    assert user
    assert check_password(plain_text="test-pw", hashed_password=user.password)

def test_sign_up_409(client, test_user):
    # given

    # when
    response = client.post(
        "/users/sign-up",
        json={"username": test_user.username, "password": "test-pw"},
    )

    # then
    assert response.status_code == 409


def test_log_in(client, test_session, test_user):
    # given

    # when
    response = client.post(
        "/users/login",
        json={"username": "test", "password": "test-pw"}
    )

    # then
    assert response.status_code == 200

    assert Schema({"access_token": str}).validate(response.json())

    access_token = response.json()["access_token"]
    assert access_token
    payload = _decode_access_token(access_token=access_token)
    assert payload["username"] == "test"

def test_get_me_404(client, test_session):
    # given: 유저가 없을 때
    access_token = create_access_token(username="test")

    # when
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # then: 404 Not Found
    assert response.status_code == 404

def test_get_me_200(client, test_session, test_user):
    # given: 유저가 있을 때
    access_token = create_access_token(username="test")

    # when
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # then: 200 성공
    assert response.status_code == 200
    assert Schema(
        {
            "id": int,
            "username": "test",
            "created_at": str,
        }
    ).validate(response.json())


def test_update_me(client, test_session, test_user):
    # given
    access_token = create_access_token(username="test")

    # when
    response = client.patch(
        "/users/me",
        json={"new_password": "new-test-pw"},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # then
    assert response.status_code == 200
    assert Schema(
        {
            "id": int,
            "username": "test",
            "created_at": str,
        }
    ).validate(response.json())

    user = test_session.query(User).filter(User.username == "test").first()
    assert check_password(plain_text="new-test-pw", hashed_password=user.password)


def test_delete_me(client, test_session, test_user):
    # given
    access_token = create_access_token(username="test")

    # when
    response = client.delete(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # then
    assert response.status_code == 204
    assert test_session.query(User).filter(User.username == test_user.username).first() is None


def test_get_user(client, test_session, test_user):
    # given
    new_password = hash_password(plain_text="test-pw2")
    new_user = User.create(username="test2", password=new_password)  # 조회할 대상
    test_session.add(new_user)
    test_session.commit()

    access_token = create_access_token(username=test_user.username)

    # when
    response = client.get(
        f"/users/{new_user.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # then
    assert response.status_code == 200
    assert Schema(
        {
            "id": new_user.id,
            "username": new_user.username,
            "created_at": new_user.created_at.isoformat(),
        }
    ).validate(response.json())
