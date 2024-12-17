from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy.orm import Session
from repository.database import Base, engine, get_db
from models.user import User
from models.dish import Dish
import bcrypt  
from middlewares.is_authenticated import is_authenticated
from config import ALGORITHM, SECRET_KEY

app = FastAPI()

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Modèle pour les données de connexion
class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    # Rechercher l'utilisateur dans la base de données
    print(data)
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Vérifier le mot de passe avec bcrypt
    if not bcrypt.checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Générer un JWT avec une durée de validité d'un jour
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    token = jwt.encode({"user_id": user.id, "exp": expire, "is_admin": user.is_admin}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "username": user.username,
        "token": token
    }

class SignUpData(BaseModel):
    username: str  
    password: str 
    is_admin: bool 

@app.post("/sign_up")
def sign_up(data: SignUpData, payload: dict = Depends(is_authenticated)):
    # Vérifier si l'utilisateur actuel est admin
    is_admin = payload.get("is_admin")
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    # Afficher les données reçues
    print(f"Nom d'utilisateur reçu : {data.username}")
    print(f"Mot de passe reçu : {data.password}")
    print(f"Est administrateur : {data.is_admin}")

    return {
        "message": "Sign-up data received",
        "username": data.username,
        "is_admin": data.is_admin
    }

@app.get("/")
def hello_world():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn

    host = "127.0.0.1"
    port = 8080
    print(f"Your application is running on http://{host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )