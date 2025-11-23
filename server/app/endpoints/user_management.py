from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import CreateAdminRequest, UpdateAdminRequest
from app.utils.auth_util import hash_password
from app.dependencies.auth_dependency import has_permission
from app.models.enums import UserType
from app.models.user import User
from datetime import datetime


router = APIRouter(prefix="/user-management", tags=["User Management"])


#===========================
#      Admin Endpoints
#===========================

@router.post("/users", status_code=status.HTTP_201_CREATED)
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


@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user_admin(
    user_id: int,
    request_data: UpdateAdminRequest,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):

    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if request_data.name and request_data.name != existing_user.name: 
        existing_user.name = request_data.name

    if request_data.phone and request_data.phone != existing_user.phone: 
        existing_user.phone = request_data.phone

    if request_data.address and request_data.address != existing_user.address: 
        existing_user.address = request_data.address

    if request_data.password:
        existing_user.password = hash_password(request_data.password)

    if request_data.email and request_data.email != existing_user.email:
        email_exists = db.query(User).filter(User.email == request_data.email).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        existing_user.email = request_data.email

    existing_user.updated_by = user_info["username"]
    existing_user.updated_at = datetime.utcnow()

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)