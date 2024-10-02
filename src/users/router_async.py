from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Path, status, HTTPException, Depends, Body, BackgroundTasks

from core.authentication.hashing import hash_password, check_password
from core.authentication.jwt import JWTService
from core.authentication.dependency import get_username
from core.database.connection_async import get_async_db
from core.email import send_email

from users.models import User
from users.request import UserAuthRequest
from users.response import UserResponse, UserTokenResponse


router = APIRouter(prefix="/async/users", tags=["Async Users"])


@router.post(
	"/sign-up",
	status_code=status.HTTP_201_CREATED,
	response_model=UserResponse,
)
async def sign_up_user_handler(
	body: UserAuthRequest,
	background_tasks: BackgroundTasks,
	db: AsyncSession = Depends(get_async_db),
):
	new_user = User.create(
		username=body.username,
		password=hash_password(plain_text=body.password)
	)
	db.add(new_user)
	await db.commit()
	background_tasks.add_task(send_email, "회원가입을 축하합니다!")
	return UserResponse.build(user=new_user)


@router.post(
	"/login",
	status_code=status.HTTP_200_OK,
	response_model=UserTokenResponse,
)
async def login_user_handler(
	body: UserAuthRequest,
	db: AsyncSession = Depends(get_async_db),
	jwt_service: JWTService = Depends(),
):
	result = await db.execute(select(User).filter(User.username == body.username))
	user: User | None = result.scalars().first()  # sqlalchemy가 db에서 가져온 정보
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

	access_token = jwt_service.create_access_token(username=user.username)
	return UserTokenResponse.build(access_token=access_token)


@router.get(
	"/me",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
async def get_me_handler(
	username: str = Depends(get_username),
	db: AsyncSession = Depends(get_async_db),
):
	result = await db.execute(select(User).filter(User.username == username))
	user: User | None = result.scalars().first()
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
async def update_me_handler(
	username: str = Depends(get_username),
	new_password: str = Body(..., embed=True),
	db: AsyncSession = Depends(get_async_db),
):
	result = await db.execute(select(User).filter(User.username == username))
	user: User | None = result.scalars().first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)

	new_password_hash: str = hash_password(plain_text=new_password)
	user.update_password(new_password=new_password_hash)

	db.add(user)
	await db.commit()
	return UserResponse.build(user=user)


@router.delete(
	"/me",
	status_code=status.HTTP_204_NO_CONTENT,
	response_model=None,
)
async def delete_me_handler(
	username: str = Depends(get_username),
	db: AsyncSession = Depends(get_async_db),
):
	result = await db.execute(select(User).filter(User.username == username))
	user: User | None = result.scalars().first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)

	await db.delete(user)
	await db.commit()


@router.get(
	"/{user_id}",
	status_code=status.HTTP_200_OK,
	response_model=UserResponse,
)
async def get_user_handler(
	user_id: int = Path(default=..., ge=1),
	_: str = Depends(get_username),
	db: AsyncSession = Depends(get_async_db),
):
	result = await db.execute(select(User).filter(User.id == user_id))
	user: User | None = result.scalars().first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found",
		)
	return UserResponse.build(user=user)
