import datetime # used to find the date
import httpx # used to fetch/retrieve data from external APIs
from fastapi import APIRouter, Depends, HTTPException, status # used to retrieve specific routes for router, use for database dependency, return errors and specific statuses
from fastapi.responses import RedirectResponse # used to send user to different url
from fastapi.security import OAuth2PasswordBearer # used to retrieve jwt from Authorization header on protected requests
from sqlalchemy.orm import Session # used for type hinting
from sqlalchemy import select # used in queries
from typing import Annotated # using as a parameter for db
from jose import jwt # used to decode third party tokens
import jwt as pyjwt # used to encode/decode self created tokens
# importing objects, functions, and variables from other files
from models import User
from database import get_db
from config import CLIENT_ID, CLIENT_SECRET, SECRET_KEY, REDIRECT_URI, ALGORITHM, JWT_ALGORITHM

router = APIRouter() # initializes router

@router.get("/auth/google")
def get_auth():
    return RedirectResponse(url=f"https://accounts.google.com/o/oauth2/auth?scope=email%20profile&response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}") #redirects user to google auth page

@router.get("/auth/google/callback")
def get_callback(code:str, db: Annotated[Session, Depends(get_db)]):
    res = httpx.post(url="https://oauth2.googleapis.com/token", data={"client_id":CLIENT_ID, "client_secret":CLIENT_SECRET,"code":code,"redirect_uri":REDIRECT_URI,"grant_type":"authorization_code"}) # Sends user data to token url
    token_data = res.json()
    id_token = token_data["id_token"]
    user_info=jwt.decode(id_token,"",[ALGORITHM],options={"verify_signature": False, "verify_at_hash": False},audience=CLIENT_ID)
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
    } # JWT payload containing user email and expiration date
    encoded = pyjwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM) # Encodes JWT

    return encoded
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/google/callback") # Retrieves JWT from Auth header
def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2_scheme)):
    try: # only runs if the token is valid
        current_user=pyjwt.decode(token,SECRET_KEY,[JWT_ALGORITHM]) # decodes JWT to find user data
        query = (
            select(User)
            .where(User.email==current_user["sub"])
        )
        sub_check = db.execute(query).scalars().first() # queries user email
        if sub_check:
            return sub_check
        else: # returns invalid if email not in database
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Not a current user"
            )
    except pyjwt.InvalidTokenError:
         raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Not a current user"
                )