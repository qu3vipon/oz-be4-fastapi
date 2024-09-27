from sqlalchemy.orm import Session
from fastapi import APIRouter, Path, status, HTTPException, Depends, Body

from core.authentication.hashing import hash_password, check_password
from core.authentication.jwt import create_access_token, get_username
from core.database.connection import get_db

from users.models import User
from users.repository import UserRepository
from users.request import UserAuthRequest
from users.response import UserResponse, UserTokenResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
	"/sign-up",
	status_code=status.HTTP_201_CREATED,
	response_model=UserResponse,
)
def sign_up_user_handler(
	body: UserAuthRequest,
	user_repo: UserRepository = Depends(),
):
	new_user = User.create(
		username=body.username,
		password=hash_password(plain_text=body.password)
	)
	user_repo.save(user=new_user)
	return UserResponse.build(user=new_user)


@router.post(
	"/login",
	status_code=status.HTTP_200_OK,
	response_model=UserTokenResponse,
)
def login_user_handler(
	body: UserAuthRequest,
	user_repo: UserRepository = Depends(),
):
	user: User | None = user_repo.get_user_by_username(username=body.username)

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
	user_repo: UserRepository = Depends(),
):
	user: User | None = user_repo.get_user_by_username(username=username)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return UserResponse.build(user=user)


@router.patch(
	"/me",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
def update_me_handler(
	username: str = Depends(get_username),
	new_password: str = Body(..., embed=True),
	user_repo: UserRepository = Depends(),
):
	user: User | None = user_repo.get_user_by_username(username=username)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)

	user.update_password(new_password=hash_password(plain_text=new_password))
	user_repo.save(user=user)
	return UserResponse.build(user=user)


@router.delete(
	"/me",
	status_code=status.HTTP_204_NO_CONTENT,
	response_model=None,
)
def delete_me_handler(
	username: str = Depends(get_username),
	user_repo: UserRepository = Depends(),
):
	user: User | None = user_repo.get_user_by_username(username=username)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	user_repo.delete_user(user)



@router.get(
	"/{user_id}",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
def get_user_handler(
	user_id: int = Path(default=..., ge=1),
	_: str = Depends(get_username),
	user_repo: UserRepository = Depends(),
):
	user: User | None = user_repo.get_user_by_id(user_id=user_id)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return UserResponse.build(user=user)
