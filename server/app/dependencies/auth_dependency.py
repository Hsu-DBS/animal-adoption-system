from typing import List
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

def has_permission(required_roles: str | List[str]):
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def dependency(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {', '.join(required_roles)}"
            )
        return user

    return dependency
