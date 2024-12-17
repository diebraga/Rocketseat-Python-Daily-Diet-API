from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from config import ALGORITHM, SECRET_KEY

# Middleware de sécurité HTTPBearer
security = HTTPBearer()

# Fonction pour vérifier le JWT
def is_authenticated(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retourne les données extraites du token
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")