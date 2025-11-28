from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.application import Application
from app.models.animal import Animal
from app.models.enums import AdoptionStatus, ApplicationStatus, UserType
from app.schemas.general_schema import GeneralResponse
from app.dependencies.auth_dependency import has_permission
from datetime import datetime
from app.schemas.application_schema import CreateApplicationRequest, UpdateApplicationStatusRequest
from app.utils.common_util import paginate_query

router = APIRouter(prefix="/application-management", tags=["Application Management"])


@router.get(
    "/applications",
    response_model=GeneralResponse,
)
def get_all_applications(
    page: int = Query(1, ge=1, description="Page number must be >= 1"),
    limit: int = Query(10, ge=1, le=100, description="Limit must be between 1 and 100"),
    db: Session = Depends(get_db),
    _ = Depends(has_permission("Admin"))
):
    # Query active applications
    query = (
        db.query(Application)
        .filter(Application.is_deleted.is_(False))
        .order_by(Application.id.asc())
    )

    # Pagination
    paginated = paginate_query(query, page, limit)

    applications = []
    for app in paginated["query_data"]:
        applications.append({
            "id": app.id,
            "animal_id": app.animal_id,
            "animal_name": app.animal.name,   
            "adopter_id": app.adopter_id,
            "adopter_name": app.adopter.name,  
            "reason": app.reason,
            "status": app.application_status.value,
            "created_at": app.created_at,
            "created_by": app.created_by,
            "updated_at": app.updated_at,
            "updated_by": app.updated_by,
        })

    data_to_return = {
        "page": paginated["page"],
        "limit": paginated["limit"],
        "total": paginated["total"],
        "total_pages": paginated["total_pages"],
        "applications": applications
    }

    return GeneralResponse(
        message="Applications retrieved successfully",
        data=data_to_return
    )


@router.get(
    "/applications/current-adopter",
    response_model=GeneralResponse,
)
def get_applications_of_current_adopter(
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Adopter"))
):
    adopter_id = int(user_info["sub"])

    # Get all active applications for current login adopter
    applications = (
        db.query(Application)
        .filter(
            Application.adopter_id == adopter_id,
            Application.is_deleted.is_(False)
        )
        .order_by(Application.id.asc())
        .all()
    )

    application_list = [
        {
            "id": app.id,
            "animal_id": app.animal_id,
            "animal_name": app.animal.name,
            "status": app.application_status.value,
            "reason": app.reason,
            "created_at": app.created_at,
            "created_by": app.created_by,
            "updated_at": app.updated_at,
            "updated_by": app.updated_by,
        }
        for app in applications
    ]

    return GeneralResponse(
        message="Applications retrieved successfully",
        data={"applications": application_list}
    )


@router.get(
    "/applications/{application_id}",
    response_model=GeneralResponse,
)
def get_application_by_id(
    application_id: int,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission(["Admin", "Adopter"]))  #allow access for admin and adopter roles
):
    # Get application
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.is_deleted.is_(False)
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    # If adopter, only allow viewing their own application
    role = user_info["role"]
    current_user_id = int(user_info["sub"])

    if role == UserType.Adopter.value and application.adopter_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this application"
        )

    # response data
    app_info = {
        "id": application.id,
        "animal_id": application.animal_id,
        "animal_name": application.animal.name,
        "adopter_id": application.adopter_id,
        "adopter_name": application.adopter.name,
        "reason": application.reason,
        "status": application.application_status.value,
        "created_at": application.created_at,
        "created_by": application.created_by,
        "updated_at": application.updated_at,
        "updated_by": application.updated_by,
    }

    return GeneralResponse(
        message="Application retrieved successfully",
        data=app_info
    )


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )
    
    # cannot apply if animal is already adopted
    if animal.adoption_status == AdoptionStatus.Adopted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This animal has already been adopted. Applications are no longer accepted."
        )

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already submitted an application for this animal"
        )

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


#Using PATCH because only one field(application_status) is being updated
@router.patch(
    "/applications/{application_id}/status",
    status_code=status.HTTP_204_NO_CONTENT
)
def update_application_status(
    application_id: int,
    request_data: UpdateApplicationStatusRequest,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))  # only admin can change status
):
    # Fetch application
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.is_deleted.is_(False)
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    # Prevent changing status after Approved/Rejected
    if application.application_status in [ApplicationStatus.Approved, ApplicationStatus.Rejected]:
        raise HTTPException(400, "Cannot modify a completed application")

    # Update application status
    application.application_status = request_data.application_status
    application.updated_at = datetime.utcnow()
    application.updated_by = user_info["username"]

    db.commit()
    db.refresh(application)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
