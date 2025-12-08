from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Animal, User, Application
from app.schemas.general_schema import GeneralResponse
from app.dependencies.auth_dependency import has_permission
from app.models.enums import ApplicationStatus, UserType

router = APIRouter(prefix="/dashboard-management", tags=["Dashboard Management"])

@router.get(
    "/dashboard/summary",
    response_model=GeneralResponse
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    _ = Depends(has_permission(["Admin"])),
):

    # Count animals
    total_animals = db.query(Animal).filter(
        Animal.is_deleted.is_(False)
    ).count()

    # Pending applications
    pending_applications = db.query(Application).filter(
        Application.is_deleted.is_(False),
        Application.application_status == ApplicationStatus.Submitted
    ).count()

    # Approved applications
    approved_applications = db.query(Application).filter(
        Application.is_deleted.is_(False),
        Application.application_status == ApplicationStatus.Approved
    ).count()

    # Count adopters
    total_adopters = db.query(User).filter(
        User.is_deleted.is_(False),
        User.user_type == UserType.Adopter
    ).count()

    data = {
        "total_animals": total_animals,
        "total_pending_applications": pending_applications,
        "total_approved_applications": approved_applications,
        "total_adopters": total_adopters,
    }

    return GeneralResponse(
        message="Dashboard summary retrieved successfully",
        data=data
    )
