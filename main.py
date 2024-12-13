from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy.orm import Session
from repository.database import Base, engine, get_db
from models.user import User
from models.dish import Dish
import bcrypt  # Import bcrypt

# Clé secrète et algorithme pour JWT
SECRET_KEY = "45tyhjhYGHJ£$%TGHj5yuuuuyghGGDSSEbH&**^"
ALGORITHM = "HS256"

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
    token = jwt.encode({"user_id": user.id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "username": user.username,
        "token": token
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