from sqlmodel import Field, SQLModel

from schemas.role import Role


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    name: str
    role: Role

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int