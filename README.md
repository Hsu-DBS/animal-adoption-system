# Digital Animal Adoption System

The **Digital Animal Adoption System** is a full-stack web application developed to support and modernize the animal adoption process for animal shelters. It provides a structured, secure, and user-friendly platform for managing animals, adopters, administrators, and adoption applications.

The system supports the complete adoption workflow for both administrators and adopters. Administrators manage animal records, upload images, review adoption applications, and monitor system activity through an administrative dashboard. Adopters can browse available animals, view their details, and submit adoption applications. Once an application is approved, the animal’s status is automatically updated to prevent further applications, ensuring a clear and well-controlled adoption process.

The system is built using **FastAPI**, **React (Vite)**, and **PostgreSQL**, and is deployed on **Render**.  
For local development and testing, **SQLite** is used to simplify setup and development.

---

## Project Context & Location

This system is designed for an animal shelter located in Yangon, Myanmar.

📍 **Google Maps Location:**  
https://maps.app.goo.gl/jFosJcP3p4g4kFDz9

---

## Live Application Links

- **Backend API (Swagger):**  
  https://animal-adoption-backend-k5ty.onrender.com/docs

- **Admin Login (Frontend):**  
  https://animal-adoption-frontend.onrender.com/#/admin/login

- **Adopter Login (Frontend):**  
  https://animal-adoption-frontend.onrender.com/#/login

---

## Technologies Used

### Backend
- **FastAPI** – High-performance Python web framework
- **SQLAlchemy** – ORM for database management
- **Pydantic** – Data validation
- **JWT Authentication** – Secure role-based authentication
- **Pytest** – Unit testing framework
- **Uvicorn** – ASGI server

### Frontend
- **React (Vite)** – Modern frontend framework
- **CSS Modules** – Component-scoped styling
- **Axios** – API communication with interceptors
- **React Router** – Client-side routing

### Database
- **SQLite** – Local development and testing
- **PostgreSQL** – Production database (Render)

### Deployment
- **Render**
  - Web Service (FastAPI backend)
  - Static Site (React frontend)
  - PostgreSQL database (Free tier)

---

## Project Structure (Overview)

```text
client/    – React (Vite) frontend
server/    – FastAPI backend
tests/     – Pytest unit tests
```

---

## User Roles & Features

### Admin
- Login as administrator
- Create, update, and delete animals
- View all adoption applications
- Approve or reject applications
- Manage adopters
- Manage admin users
- View dashboard statistics
- Update own profile

### Adopter
- Register and login
- Browse available animals
- Search and filter animals
- Submit adoption applications
- View application history
- Update own profile

---

## Admin Dashboard

The admin dashboard provides system-level insights, including:
- Total animals
- Pending applications
- Approved applications
- Rejected applications
- Total adopters
- Total admins

This allows administrators to monitor adoption activity efficiently.

---

## Testing

Backend unit tests are implemented using **Pytest** and **FastAPI TestClient**.

### Covered Test Scenarios
- Admin login
- Create animal
- Submit adoption application
- Approve application and update animal status

### Test Database
- Uses **SQLite**
- Tables are created and dropped automatically during test sessions
- Production database is never affected

### Run Tests
```bash
cd server
python -m pytest
```

---

## How to Run the Project Locally

### Backend (FastAPI)

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to backend
cd server

# Run backend server
uvicorn app.main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### Frontend (React)

```bash
cd client/my-react-app
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

### Run Unit Tests

```bash
cd server
python -m pytest
```

---

## Environment Variables

### Local Development (`.env`)
```env
SECRET_KEY=secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=120
IMAGE_DIR=server/app/src/images
```

### Production (Render)
Set the following environment variables in Render:
- `DATABASE_URL` (PostgreSQL connection string)
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `IMAGE_DIR`

---

## Deployment (Render)

- Backend deployed as a **Render Web Service**
- Frontend deployed as a **Render Static Site**
- PostgreSQL used as the production database
- Environment variables configured in Render dashboard
- Initial admin account created using `initial_data.py`

---

## References & Acknowledgements

During the development of this project, several online resources were used for learning and guidance. Some of these reference links were not added directly to the related source files at the time, so they are listed here for completeness.

- FastAPI file upload guide:  
  https://fastapi.tiangolo.com/tutorial/request-files/

- Explanation of the difference between PUT and PATCH requests:  
  https://www.geeksforgeeks.org/javascript/difference-between-put-and-patch-request/

Parts of the backend project structure were inspired by an MVC-style organization described in the following article:

- FastAPI MVC Project Structure:  
  https://verticalserve.medium.com/building-a-python-fastapi-crud-api-with-mvc-structure-13ec7636d8f2

Additional reference links are included at the top of relevant source files, and some references are also mentioned in the corresponding Git commit messages.

---

## Implemented By

**Hsu Myint Myat Kyaw**  
Student ID: 20084781

---

## Project Status

- Backend completed  
- Frontend completed  
- Unit testing implemented  
- Deployed on Render  

---

Thank you for reviewing this project 🙏