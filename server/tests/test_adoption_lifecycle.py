# References:
# https://fastapi.tiangolo.com/tutorial/testing/#using-testclient
# https://docs.python.org/3/library/io.html#io.BytesIO
# https://docs.pytest.org/en/stable/how-to/assert.html


# Used to create an in-memory file object (BytesIO) for image upload testing
import io
import json


# common login function and return access token
def login_user(client, email, password, role):
    response = client.post(
        f"/auth/login/{role}",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    token = response.json()["data"]["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# Create animal as admin and return animal_id
def create_animal(client, headers, animal_data):
    files = {
        "request_data": (
            None,
            json.dumps(animal_data),
            "application/json",
        ),
        "animal_image": (
            "dog.jpg",
            io.BytesIO(b"fake-image-content"),
            "image/jpeg",
        ),
    }

    response = client.post(
        "/animal-management/animals",
        headers=headers,
        files=files,
    )

    assert response.status_code == 201
    return response.json()["data"]["id"]


# TEST 1: Create animal
def test_create_animal(client, test_admin):
    # Login as admin
    admin_headers = login_user(
        client,
        test_admin["email"],
        test_admin["password"],
        role="admin",
    )

    # Animal payload
    animal_data = {
        "name": "Test Dog",
        "species": "Dog",
        "breed": "Labrador",
        "age": 3,
        "gender": "Male",
        "description": "Friendly test dog",
        "adoption_status": "Available",
    }

    # Create animal
    animal_id = create_animal(client, admin_headers, animal_data)

    # Basic assertion
    assert animal_id is not None


# TEST 2: Submit adoption application
def test_submit_application(client, test_admin, test_adopter):

    # Login as admin to obtain JWT token bcuz admin is required to create animal
    admin_headers = login_user(
        client,
        test_admin["email"],
        test_admin["password"],
        role="admin",
    )

    # Create a test animal that can be adopted
    animal_id = create_animal(
        client,
        admin_headers,
        {
            "name": "Apply Dog",
            "species": "Dog",
            "breed": "Beagle",
            "age": 2,
            "gender": "Male",
            "description": "Dog for application test",
            "adoption_status": "Available",
        },
    )

    # Login as adopter to obtain JWT token & to submit adoption application
    adopter_headers = login_user(
        client,
        test_adopter["email"],
        test_adopter["password"],
        role="adopter",
    )

    # Submit adoption application for the created animal
    response = client.post(
        "/application-management/applications",
        headers=adopter_headers,
        json={
            "animal_id": animal_id,
            "reason": "I want to adopt this dog",
        },
    )

    # Verify that the application was created successfully
    assert response.status_code == 201
    assert response.json()["message"] == "Application submitted successfully"


# TEST 3: Update application status
def test_update_application_status(client, test_admin, test_adopter):

    # Admin login
    admin_headers = login_user(
        client,
        test_admin["email"],
        test_admin["password"],
        role="admin"
    )

    # Admin creates an animal
    animal_id = create_animal(
        client,
        admin_headers,
        {
            "name": "Approve Dog",
            "species": "Dog",
            "breed": "Husky",
            "age": 4,
            "gender": "Male",
            "description": "Dog for approval test",
            "adoption_status": "Available",
        }
    )

    # Adopter login
    adopter_headers = login_user(
        client,
        test_adopter["email"],
        test_adopter["password"],
        role="adopter"
    )

    # Adopter submits adoption application
    app_response = client.post(
        "/application-management/applications",
        headers=adopter_headers,
        json={
            "animal_id": animal_id,
            "reason": "I want this dog",
        },
    )

    # Verify application creation success
    assert app_response.status_code == 201

    # Extract application ID from response
    application_id = app_response.json()["data"]["id"]

    # Admin approves the application
    update_response = client.patch(
        f"/application-management/applications/{application_id}/status",
        headers=admin_headers,
        json={"application_status": "Approved"},
    )

    # Verify successful status update
    assert update_response.status_code == 204

    # Verify animal status is updated to "Adopted"
    animals_res = client.get(
        "/animal-management/animals",
        headers=admin_headers,
    )

    # Extract animals list from response
    animals = animals_res.json()["data"]["animals"]

    # Find the updated animal by ID
    updated_animal = next(a for a in animals if a["id"] == animal_id)

    # Confirm adoption status has changed correctly
    assert updated_animal["adoption_status"] == "Adopted"
