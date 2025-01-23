from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from typing import Optional
from datetime import datetime, timedelta
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
database = client['auth_template']
users_collection = database['users']

SECRET_KEY = os.getenv("SECRET_KEY")  

class User(BaseModel):
    name: str
    email: EmailStr
    password_hash: Optional[str] = None
    google_id: Optional[str] = None
    picture: Optional[str] = None
    is_verified: bool = False

    @classmethod
    def from_google(cls, google_user_info: dict):
        return cls(
            name=google_user_info['name'],
            email=google_user_info['email'],
            google_id=google_user_info['sub'],
            picture=google_user_info.get('picture')
        )

    def save_to_db(self):
        users_collection.update_one(
            {"email": self.email},
            {"$set": self.dict()},
            upsert=True
        )

    @classmethod
    def find_by_email(cls, email: str):
        user_data = users_collection.find_one({"email": email})
        if user_data:
            return cls(**user_data)
        return None

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        if self.password_hash:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        return False

    def generate_reset_token(self):
        token = jwt.encode(
            {"email": self.email, "exp": datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        users_collection.update_one(
            {"email": self.email},
            {"$set": {"reset_token": token}}
        )
        return token

    @staticmethod
    def verify_reset_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            email = payload["email"]
            user_data = users_collection.find_one({"email": email, "reset_token": token})
            if user_data:
                return email
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return None

    @staticmethod
    def remove_reset_token(token: str):
        users_collection.update_one(
            {"reset_token": token},
            {"$unset": {"reset_token": ""}}
        )
        
        
        