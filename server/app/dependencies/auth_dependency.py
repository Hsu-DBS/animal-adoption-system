from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.utils.auth_util import SECRET_KEY, ALGORITHM
from app.models.enums import UserType

security = HTTPBearer()  # Use HTTPBearer() to read Bearer tokens from Authorization header


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        #decode JWT token to get payloads
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # payload={"sub":1, "username":"Admin", "role":"Admin"}
    except JWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def has_permission(required_role: str):
    def dependency(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role} access only"
            )
        return user
    return dependency


