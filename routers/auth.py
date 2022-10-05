from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.data import get_connection


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

con, cur = get_connection()


def get_user(name: str):
    cur.execute("SELECT * FROM user WHERE name = (?)", (name,))
    row = cur.fetchone()
    if row is not None:
        return dict(row)


def decode_token(token):
    # This doesn't provide any security at all
    user = get_user(token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cur.execute("SELECT * FROM user WHERE name = (?)", (form_data.username,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=400, detail="Incorrect name or sex")
    sex = row['sex']
    if not form_data.password == sex:
        raise HTTPException(status_code=400, detail="Incorrect name or sex")

    return {"access_token": row['name'], "token_type": "bearer"}


@router.get("/me")
async def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
