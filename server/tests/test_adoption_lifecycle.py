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
