from sqlalchemy.orm.session import Session

from schemas.user import User


def user_exists(username: str, session: Session)-> bool:
    return session.query(User).filter(User.username == username).first() is not None
