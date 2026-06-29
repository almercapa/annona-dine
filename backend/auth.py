import datetime
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from jose import jwt
import jwt as pyjwt
from models import User
from database import get_db
from config import CLIENT_ID, CLIENT_SECRET, SECRET_KEY, REDIRECT_URI, ALGORITHM, JWT_ALGORITHM

router = APIRouter()

@router.get("/auth/google")
def get_auth():
    return RedirectResponse(url=f"https://accounts.google.com/o/oauth2/auth?scope=email%20profile&response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}")

@router.get("/auth/google/callback")
def get_callback(code:str,db: Annotated[Session, Depends(get_db)]):
    res = httpx.post(url="https://oauth2.googleapis.com/token", data={"client_id":CLIENT_ID, "client_secret":CLIENT_SECRET,"code":code,"redirect_uri":REDIRECT_URI,"grant_type":"authorization_code"})
    token_data = res.json()
    id = token_data["id_token"]
    user_info=jwt.decode(id,"",[ALGORITHM],options={"verify_signature": False, "verify_at_hash": False},audience=CLIENT_ID)
    if user_info["hd"] != "scarletmail.rutgers.edu":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Must use a Rutgers ScarletMail account"
        )
    query = (
        select(User)
        .where(User.email==user_info["email"])
    )
    user_check = db.execute(query).scalars().first()
    if not user_check:
        new_user = User(first_name=user_info["given_name"],last_name=user_info["family_name"],email=user_info["email"],profile_picture=user_info["picture"])
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    payload = {
        "sub": user_info["email"],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    }
    encoded = pyjwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google/callback")
def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2_scheme)):
    try:
            current_user=pyjwt.decode(token,SECRET_KEY,[JWT_ALGORITHM])
            current_sub = current_user["sub"]
            query = (
                select(User)
                .where(User.email==current_user["sub"])
            )
            sub_check = db.execute(query).scalars().first()
            if sub_check:
                return sub_check
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Not a current user"
                )
    except pyjwt.InvalidTokenError:
         raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Not a current user"
                )