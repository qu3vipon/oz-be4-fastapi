from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, status, HTTPException, Depends

from core.authentication.hashing import hash_password, check_password
from core.authentication.jwt import create_access_token, get_username
from core.database.connection import get_db

from users.models import User
from users.request import UserAuthRequest, UpdateUserRequest
from users.response import UserResponse, UserTokenResponse

users = [
	{"id": 1, "username": "elon", "password": "$2b$12$QTOwKB4oX.2e11YOu4Kx7eUjESZqJVmRkY7ARu01.ZhvLDeQ80Eia"},
]

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
	"/sign-up",
	status_code=status.HTTP_201_CREATED,
	response_model=UserResponse,
)
def sign_up_user_handler(
	body: UserAuthRequest,
	db: Session = Depends(get_db),
):
	new_user = User.create(
		username=body.username,
		password=hash_password(plain_text=body.password)
	)
	db.add(new_user)
	db.commit()
	return UserResponse.build(user=new_user)


@router.post(
	"/login",
	status_code=status.HTTP_200_OK,
	response_model=UserTokenResponse,
)
def login_user_handler(
	body: UserAuthRequest,
	db: Session = Depends(get_db),
):
	# SELECT * FROM service_user WHERE username = body.username
	user: User | None = db.query(User).filter(User.username == body.username).first()

	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)

	if not check_password(plain_text=body.password, hashed_password=user.password):
		raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Unauthorized",
			)

	access_token = create_access_token(username=user.username)
	return UserTokenResponse.build(access_token=access_token)





@router.get(
	"/me",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
def get_me_handler(
	username: str = Depends(get_username),
	db: Session = Depends(get_db),
):
	user: User | None = db.query(User).filter(User.username == username).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return UserResponse.build(user=user)


@router.get(
	"/{user_id}",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
def get_user_handler(user_id: int = Path(default=..., ge=1)):
	for user in users:
		if user["id"] == user_id:
			return UserResponse.build(user=user)

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="User not found",
	)



@router.patch(
	"/{user_id}",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
def update_user_handler(user_id: int, body: UpdateUserRequest):
	for user in users:
		if user["id"] == user_id:
			user["username"] = body.username
			return UserResponse.build(user=user)

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="User not found",
	)

@router.delete(
	"/{user_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	response_model=None,
)
def delete_user_handler(user_id: int):
	for user in users:
		if user["id"] == user_id:
			users.remove(user)
			return None

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="User not found",
	)
