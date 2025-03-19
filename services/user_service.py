from sqlalchemy import select
from sqlalchemy.orm import Session

from models.ocd import OcdArticleDB, OcdUserDB, UserRole
from services import auth_service


def get_user_by_email(session: Session, email: str) -> OcdUserDB | None:
    stmt = select(OcdUserDB).where(OcdUserDB.email == email)
    user = session.execute(stmt).scalar()
    return user


def create_user(session: Session, email: str, password: str):
    user_db = OcdUserDB(
        email=email,
        role=UserRole.USER,
        hashed_password=auth_service.get_password_hash(password),
    )
    session.add(user_db)
    session.commit()
    return user_db.id
