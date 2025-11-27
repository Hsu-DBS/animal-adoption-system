import os
import json
from dotenv import load_dotenv
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.db.database import get_db
from app.models.animal import Animal
from app.schemas.animal_schema import CreateAnimalRequest
from app.schemas.general_schema import GeneralResponse
from app.utils.common_util import paginate_query
from app.dependencies.auth_dependency import has_permission


router = APIRouter(prefix="/animal-management", tags=["Animal Management"])

load_dotenv()
IMAGE_DIR = os.getenv("IMAGE_DIR")


@router.get(
    "/animals",
    response_model=GeneralResponse,
    status_code=status.HTTP_200_OK
)
def get_all_animals(
    page: int = Query(1, ge=1, description="Page number must be greater than 0"),
    limit: int = Query(10, ge=1, le=100, description="Limit must be between 1 and 100"),
    db: Session = Depends(get_db),
    _ = Depends(has_permission(["Admin", "Adopter"])),
):

    query = (
        db.query(Animal)
        .filter(Animal.is_deleted.is_(False))
        .order_by(Animal.id.asc())
    )

    # Apply pagination
    paginated_info = paginate_query(query, page, limit)

    # Format animal data
    animals = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,
            "breed": animal.breed,
            "age": animal.age,
            "gender": animal.gender,
            "description": animal.description,
            "photo_url": animal.photo_url,
            "adoption_status": animal.adoption_status.value,
            "created_at": animal.created_at,
            "created_by": animal.created_by,
            "updated_at": animal.updated_at,
            "updated_by": animal.updated_by,
        }
        for animal in paginated_info["query_data"]
    ]

    # Wrap pagination result
    data_to_return = {
        "page": paginated_info["page"],
        "limit": paginated_info["limit"],
        "total": paginated_info["total"],
        "total_pages": paginated_info["total_pages"],
        "data": animals
    }

    return GeneralResponse(
        message="Get all animals successfully",
        data=data_to_return
    )


@router.get(
    "/animals/{animal_id}",
    response_model=GeneralResponse,
    status_code=status.HTTP_200_OK
)
def get_animal_by_id(
    animal_id: int,
    db: Session = Depends(get_db),
    _ = Depends(has_permission(["Admin", "Adopter"])),
):
    # Get animal that is not soft-deleted
    animal = (
        db.query(Animal)
        .filter(
            Animal.id == animal_id,
            Animal.is_deleted.is_(False)
        )
        .first()
    )

    # If no matching animal found
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )

    # Format response data
    animal_info = {
        "id": animal.id,
        "name": animal.name,
        "species": animal.species,
        "breed": animal.breed,
        "age": animal.age,
        "gender": animal.gender,
        "description": animal.description,
        "photo_url": animal.photo_url,
        "adoption_status": animal.adoption_status.value,
        "created_at": animal.created_at,
        "created_by": animal.created_by,
        "updated_at": animal.updated_at,
        "updated_by": animal.updated_by,
    }

    return GeneralResponse(
        message="Animal retrieved successfully",
        data=animal_info
    )


@router.post(
    "/animals",
    response_model=GeneralResponse,
    status_code=status.HTTP_201_CREATED
)
def create_animal(
    request_data: str = Form(...),           #JSON string from form-data
    animal_image: UploadFile = File(...),    #Animal Image file
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin")),
):
    #Parse the JSON string into a dictionary
    try:
        request_dict = json.loads(request_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON format in request_data"
        )

    #Validate using Pydantic model
    try:
        request_data = CreateAnimalRequest(**request_dict)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
    )

    # Validate file extension
    ext = animal_image.filename.rsplit(".", 1)[-1].lower() #split once from the right at the last dot

    if ext not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Only .jpg, .jpeg, .png, .webp are allowed."
        )

    #Ensure the image directory exists
    os.makedirs(IMAGE_DIR, exist_ok=True)

    #Generate unique filename
    filename = f"{int(datetime.utcnow().timestamp())}_{animal_image.filename}"
    file_path = os.path.join(IMAGE_DIR, filename)

    #Save image file
    with open(file_path, "wb") as f:
        f.write(animal_image.file.read())

    #Build the image URL used by UI
    photo_url = f"/images/{filename}"

    #Prevent duplicate animal records
    existing_animal = (
        db.query(Animal)
        .filter(
            Animal.name == request_data.name,
            Animal.breed == request_data.breed,
            Animal.species == request_data.species,
        )
        .first()
    )

    if existing_animal:
        raise HTTPException(
            status_code=400,
            detail="Animal with similar information already exists"
        )

    #Create new animal entity
    new_animal = Animal(
        name=request_data.name,
        species=request_data.species,
        breed=request_data.breed,
        age=request_data.age,
        gender=request_data.gender,
        description=request_data.description,
        photo_url=photo_url,
        adoption_status=request_data.adoption_status,
        is_deleted=False,
        created_at=datetime.utcnow(),
        created_by=user_info["username"]
    )

    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)

    return GeneralResponse(
        message="Animal created successfully",
        data={
            "id": new_animal.id,
            "name": new_animal.name,
            "species": new_animal.species,
            "breed": new_animal.breed,
            "photo_url": new_animal.photo_url
        }
    )


