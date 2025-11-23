from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.enums import UserType
from app.schemas.login_schema import AdminLoginRequest
from app.schemas.general_schema import GeneralResponse
from app.utils.auth_util import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Auth Management"])


@router.post(
    "/login/admin",
    response_model=GeneralResponse
)
def admin_login(
    login_request_data: AdminLoginRequest,
    db: Session = Depends(get_db)
):

    try:
        # Find user
        user = db.query(User).filter(User.email == login_request_data.email).first()

        if not user:
            raise HTTPException(status_code=400, detail="Invalid email")

        # Check role
        if user.user_type != UserType.Admin.value:
            raise HTTPException(status_code=403, detail="Admin access only")

        # Check password
        if not verify_password(login_request_data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        # Create JWT token
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "username": user.name,
                "role": user.user_type,
            }
        )

        return GeneralResponse(
            message="Login successful",
            data={"access_token": access_token}
        )

    finally:
        db.close()
