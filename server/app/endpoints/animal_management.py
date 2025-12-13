# https://docs.python.org/3/library/pathlib.html
# https://www.w3schools.com/python/ref_module_pathlib.asp
# https://stackoverflow.com/questions/76451315/difference-between-pathlib-path-resolve-and-pathlib-path-parent

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query, Response
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.db.database import get_db
from app.models.animal import Animal
from app.schemas.animal_schema import CreateAnimalRequest, UpdateAnimalRequest
from app.schemas.general_schema import GeneralResponse
from app.utils.common_util import paginate_query
from app.dependencies.auth_dependency import has_permission
from app.models.enums import AdoptionStatus


router = APIRouter(prefix="/animal-management", tags=["Animal Management"])

load_dotenv()
IMAGE_DIR = os.getenv("IMAGE_DIR")


@router.get("/animals",response_model=GeneralResponse)
def get_all_animals(
    page: int = Query(1, ge=1, description="Page number must be greater than 0"),
    limit: int = Query(10, ge=1, le=100, description="Limit must be between 1 and 100"),
    search: str | None = Query(None, description="Search by name or species or breed"),
    gender: str | None = Query(None, description="Filter by gender"),
    adoption_status: str | None = Query(None, description="Filter by adoption status"),
    db: Session = Depends(get_db),
    _ = Depends(has_permission(["Admin", "Adopter"])),
):

    query = (
        db.query(Animal)
        .filter(Animal.is_deleted.is_(False))
        .order_by(Animal.id.asc())
    )

    #search by animal name, species, breed
    if search:
        query = query.filter(
            or_(
                Animal.name.ilike(f"%{search}%"),
                Animal.species.ilike(f"%{search}%"),
                Animal.breed.ilike(f"%{search}%")
            )
        )

    #filter by gender
    if gender:
        query = query.filter(Animal.gender == gender)
    
    #filter by adoption
    if adoption_status:
        query = query.filter(Animal.adoption_status == adoption_status)

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
        "animals": animals
    }

    return GeneralResponse(
        message="Get all animals successfully",
        data=data_to_return
    )


@router.get("/animals/{animal_id}", response_model=GeneralResponse)
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
            status_code=status.HTTP_400_BAD_REQUEST,
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Only .jpg, .jpeg, .png, .webp are allowed."
        )

    # Resolve the absolute base directory of the app
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Define the directory for storing animal images
    IMAGE_DIR = BASE_DIR / "src" / "images"

    # Create the images directory if it does not exist
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # generate filename
    filename = f"{int(datetime.utcnow().timestamp())}.{ext}"

    # full filepath
    file_path = IMAGE_DIR / filename

    # Save the uploaded image file
    with open(file_path, "wb") as f:
        f.write(animal_image.file.read())

    # Build the image URL to be stored in the database
    photo_url = f"/images/{filename}"

    #Prevent duplicate animal records
    existing_animal = (
        db.query(Animal)
        .filter(
            Animal.name == request_data.name,
            Animal.breed == request_data.breed,
            Animal.species == request_data.species,
            Animal.is_deleted.is_(False),
        )
        .first()
    )

    if existing_animal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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


@router.put(
    "/animals/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_animal_by_ID(
    animal_id: int,
    request_data: str | None = Form(None),
    animal_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    
    update_data = None

    if request_data:
        try:
            request_dict = json.loads(request_data) # Parse raw JSON string into dict
            update_data = UpdateAnimalRequest(**request_dict) # Validate fields using Pydantic
        except json.JSONDecodeError:
            raise HTTPException(400, "Invalid JSON format")
        except ValidationError as e:
            raise HTTPException(422, detail=e.errors())

    # Get existing animal
    animal = (
        db.query(Animal)
        .filter(
            Animal.id == animal_id,
            Animal.is_deleted.is_(False)
        )
        .first()
    )

    if not animal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Animal not found"
        )

    # Handle image upload
    if animal_image:
        # Validate extension
        filename = animal_image.filename
        ext = filename.split(".")[-1].lower()
        if ext not in ["jpg", "jpeg", "png", "webp"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .jpg, .jpeg, .png, .webp allowed"
            )

        # Save new image file
        os.makedirs(IMAGE_DIR, exist_ok=True)
        new_filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
        new_file_path = os.path.join(IMAGE_DIR, new_filename)

        with open(new_file_path, "wb") as f:
            f.write(animal_image.file.read())

        # Build new URL
        animal.photo_url = f"/images/{new_filename}"

    # Update animal fields
    if update_data:

        if update_data.name and animal.name != update_data.name:
            animal.name = update_data.name
        
        if update_data.species and animal.species != update_data.species:
            animal.species = update_data.species

        if update_data.breed and animal.breed != update_data.breed:  
            animal.breed = update_data.breed
        
        if update_data.age and animal.age != update_data.age:  
            animal.age = update_data.age

        if update_data.gender and animal.gender != update_data.gender:
            animal.gender = update_data.gender

        if update_data.description and animal.description != update_data.description:
            animal.description = update_data.description
        
        if update_data.adoption_status and animal.description != update_data.adoption_status:
            animal.adoption_status = update_data.adoption_status

    animal.updated_at = datetime.utcnow()
    animal.updated_by = user_info["username"]

    db.commit()
    db.refresh(animal)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/animals/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_animal_by_id(
    animal_id: int,
    db: Session = Depends(get_db),
    user_info = Depends(has_permission("Admin"))
):
    
    # Find animal that is not already soft deleted
    animal = (
        db.query(Animal)
        .filter(
            Animal.id == animal_id,
            Animal.is_deleted.is_(False)
        )
        .first()
    )

    # If no matching animal found, return 404
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found"
        )

    # Apply soft delete
    animal.is_deleted = True
    animal.updated_at = datetime.utcnow()
    animal.updated_by = user_info["username"]

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
