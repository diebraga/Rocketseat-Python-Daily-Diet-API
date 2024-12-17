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
def sign_up(data: SignUpData, payload: dict = Depends(is_authenticated), db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur actuel est admin
    is_admin = payload.get("is_admin")
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = db.query(User).filter(User.username == data.username).first()

    if user:
        raise HTTPException(status_code=403, detail="User already exists")

    # Hachage du mot de passe avec bcrypt
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())

    # Créer un nouvel utilisateur
    new_user = User(
        username=data.username,
        password=hashed_password.decode('utf-8'),
        is_admin=data.is_admin
    )

    # Ajouter l'utilisateur à la base de données
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { "message": "User created successfully", "username": new_user.username }


class DishData(BaseModel):
    name: str
    description: str
    is_on_diet: bool

@app.post("/create_dish")
def create_dish(data: DishData, payload: dict = Depends(is_authenticated), db: Session = Depends(get_db)):
    # Extraire user_id depuis le payload JWT
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="User ID required!")

    # Vérifier si l'utilisateur existe dans la base de données
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist!")

    dish = db.query(Dish).filter(Dish.name == data.name).first()
    if dish:
        raise HTTPException(status_code=404, detail="Dish already exist!")

    # Créer un nouveau plat (Dish)
    new_dish = Dish(
        name=data.name,
        description=data.description,
        is_on_diet=data.is_on_diet,
        user_id=user_id  
    )

    # Ajouter et sauvegarder dans la base de données
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    return {
        "message": "Dish created successfully!",
        "dish_id": new_dish.id,
        "user_id": user_id,
        "name": new_dish.name
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