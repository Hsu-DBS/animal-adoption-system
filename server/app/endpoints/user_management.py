from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.auth_util import hash_password
from app.dependencies.auth_dependency import has_permission
from app.models.enums import UserType
from app.models.user import User
from datetime import datetime
from app.utils.common_util import paginate_query
from app.schemas.general_schema import GeneralResponse
from app.schemas.user_schema import (
    CreateAdminRequest,
    UpdateAdminRequest,
    CreateAdopterRequest,
)


router = APIRouter(prefix="/user-management", tags=["User Management"])


#===========================
#      Admin Endpoints
#===========================


@router.get("/users", response_model=GeneralResponse)
def get_all_users(
    page: int = Query(1, ge=1, description="Page number must be greater than 0)"),
    limit: int = Query(10, ge=1, le=100, description="Limit must be greater than 0"),
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin")),
):
    query = db.query(User).order_by(User.id.asc())

    paginated_info = paginate_query(query, page, limit)

    users = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "user_type": user.user_type.value,
            "created_at": user.created_at,
            "created_by": user.created_by,
            "updated_at": user.updated_at,
            "updated_by": user.updated_by,
        }
        for user in paginated_info["query_data"]
    ]

    data_to_return = {
        "page": paginated_info["page"],
        "limit": paginated_info["limit"],
        "total": paginated_info["total"],
        "total_pages": paginated_info["total_pages"],
        "data": users
    }

    return GeneralResponse(
        message="Get all users successfully",
        data=data_to_return
    )


@router.get("/users/{user_id}", response_model=GeneralResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    data_to_return = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "user_type": user.user_type.value,
        "created_at": user.created_at,
        "created_by": user.created_by,
        "updated_at": user.updated_at,
        "updated_by": user.updated_by,
    }

    return GeneralResponse(
        message="Get user by ID successfully",
        data=data_to_return
    )


@router.post(
    "/users",
    response_model=GeneralResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_admin(
    request_data: CreateAdminRequest, 
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    new_user_id = _create_user(request_data, UserType.Admin, db)

    return GeneralResponse(
        message="Admin account created successfully",
        data={"id": new_user_id}
    )


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


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    # Check if user exists
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent deleting yourself
    current_user_id = int(user_info["sub"])
    if existing_user.id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )

    db.delete(existing_user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#===========================
#     Adopter Endpoints
#===========================


@router.post(
    "/adopters",
    response_model=GeneralResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_adopter(
    request_data: CreateAdopterRequest, 
    db: Session = Depends(get_db),
):
    new_user_id = _create_user(request_data, UserType.Adopter, db)

    return GeneralResponse(
        message="Adopter account created successfully",
        data={"id": new_user_id}
    )


#===========================
#     Common Functions
#===========================


def _create_user(
    request_data: dict, 
    user_type: str, 
    db: Session
):
    # Check duplicate email
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
        user_type=user_type,
        created_by="System"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user.id