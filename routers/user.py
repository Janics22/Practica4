from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import select

from db.db import SessionDep
from schemas.user import User, UserCreate, UserPublic
from services.hash import hash_password
from services.user import user_exists

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    summary="Create a new user",
    )
def create_user(*, session_dep: SessionDep, user: UserCreate) -> UserPublic:
    if user_exists(user.username, session_dep):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
            )
    hashed_password = hash_password(user.password)
    with session_dep as session:
        extra_data = {"hashed_password": hashed_password}
        db_user = User.model_validate(user, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

@router.get(
    "/",
    response_model=list[UserPublic],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all users",
    )
def get_users(*, session_dep: SessionDep) -> list[UserPublic]:
    with session_dep as session:
        users = session.exec(select(User)).all()
        return users