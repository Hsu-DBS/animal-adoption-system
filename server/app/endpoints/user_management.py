from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import CreateAdminRequest
from app.utils.auth_util import hash_password
from app.dependencies.auth_dependency import has_permission
from app.models.enums import UserType
from app.models.user import User


router = APIRouter(prefix="/user-management", tags=["User Management"])


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user_admin(
    request_data: CreateAdminRequest, 
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    # check if email exists
    existing_user = db.query(User).filter(User.email == request_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pw = hash_password(request_data.password)
    
    new_user = User(
        name=request_data.name,
        email=request_data.email,
        password=hashed_pw,
        phone=request_data.phone,
        address=request_data.address,
        user_type=UserType.Admin,
        created_by=user_info["username"]
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "id": new_user.id}