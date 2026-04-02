from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import backend.api.schemas as schemas
from backend.api.crud import AuthCrud, UserCrud
from backend.api.crud.AuthCrud import ALGORITHM, SECRET_KEY
from backend.api.dependency import get_db

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before saving!
    hashed = AuthCrud.hash_password(user.password)
    return UserCrud.create_user(db, user, hashed)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserCrud.get_user_by_username(db, form_data.username)
    if not user or not AuthCrud.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token = AuthCrud.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserCrud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
