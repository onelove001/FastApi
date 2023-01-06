from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
from schemas import UserLogin, Token
from models import User
from utils import verify
from oauth import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User with email: ({user_credentials.email}) does not exist")
    else:
        if not verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")

    access_token = create_access_token(data ={"user_id":user.id})

    return {"access_token": access_token, "token_type":"bearer"} 

