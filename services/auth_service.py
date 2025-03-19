from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import jwt
from models import generate_session
from models.ocd import OcdUserDB
from services import user_service
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "7df095938fcad8dfae20bf8ca95da6a96c6b84dd2ed9e2cb88fb982922bde9e6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# send username and password to tokenUrl url authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(
    email: str,
    password: str,
) -> OcdUserDB | bool:
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_user_by_email(email: str):
    session = next(generate_session())
    return user_service.get_user_by_email(session, email)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> OcdUserDB:
    # get current user by token which has email encrypted
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[OcdUserDB, Depends(get_current_user)],
):
    """
    add this function as Dependency to method parementer like so to resolve the authorization
    - gets user by jwt token
    - if there is jwt token -> means user was authorized
    - if there is no jwt token or is invalid or has no user in DB -> raise error
    - otherweise -> return the user for the jwt

    current_user: Annotated[User, Depends(get_current_active_user)]
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
