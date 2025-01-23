from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
from .models import User  # Remove the dot from .models
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoogleToken(BaseModel):
    token: str

@app.post("/auth/google")
async def google_auth(google_token: GoogleToken):
    try:
        # Add clock_skew_in_seconds parameter
        idinfo = id_token.verify_oauth2_token(
            google_token.token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10  # Add tolerance for clock skew
        )

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        user = User.find_by_email(idinfo['email'])
        if not user:
            user = User.from_google(idinfo)
            user.save_to_db()

        return {
            "user": {
                "name": user.name,
                "email": user.email,
                "picture": user.picture
            }
        }
    except ValueError as e:
        # Add more detailed error message
        raise HTTPException(
            status_code=400, 
            detail=f"Token verification failed: {str(e)}"
        )

@app.get("/user/me")
async def get_user_me(authorization: Optional[str] = Header(None)):
    try:
        if not authorization or not authorization.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Invalid token")
        
        token = authorization.split(' ')[1]
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            "494166917382-eacqkdr81707an52ue096q8h25h18hd6.apps.googleusercontent.com",
            clock_skew_in_seconds=10
        )

        user = User.find_by_email(idinfo['email'])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "name": user.name,
            "email": user.email,
            "picture": user.picture
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)