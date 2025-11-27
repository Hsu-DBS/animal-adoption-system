from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.application import Application
from app.models.animal import Animal
from app.models.enums import ApplicationStatus
from app.schemas.general_schema import GeneralResponse
from app.dependencies.auth_dependency import has_permission
from datetime import datetime
from pydantic import BaseModel, ValidationError
from app.schemas.application_schema import CreateApplicationRequest

router = APIRouter(prefix="/application-management", tags=["Application Management"])

@router.post(
    "/applications",
    response_model=GeneralResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    request_data: CreateApplicationRequest,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Adopter"))
):
    adopter_id = int(user_info["sub"])

    # Check animal exists and is not deleted
    animal = (
        db.query(Animal)
        .filter(
            Animal.id == request_data.animal_id,
            Animal.is_deleted.is_(False)
        ).first()
    )
    if not animal:
        raise HTTPException(404, "Animal not found")

    # Prevent duplicate active applications
    existing = (
        db.query(Application)
        .filter(
            Application.animal_id == request_data.animal_id,
            Application.adopter_id == adopter_id,
            Application.is_deleted.is_(False)
        ).first()
    )
    if existing:
        raise HTTPException(400, "You already submitted an application for this animal")

    new_app = Application(
        animal_id=request_data.animal_id,
        adopter_id=adopter_id,
        application_status=ApplicationStatus.Submitted,
        reason=request_data.reason,
        created_at=datetime.utcnow(),
        created_by=user_info["username"],
    )

    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    data_to_return = {
        "id": new_app.id,
        "animal_id": new_app.animal_id,
        "status": new_app.application_status.value
    }

    return GeneralResponse(
        message="Application submitted successfully",
        data=data_to_return
    )
