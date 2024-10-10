# Assignment Submission Portal

This is a backend system for an assignment submission portal developed using FastAPI and MongoDB. It allows two types of users—students (users) and admins to interact through various API endpoints. Users can upload assignments, and admins can accept or reject them.

## Features

- **User functionalities:**
  
  - Register and log in.
  - Upload assignments.
  - Fetch a list of available admins.
- **Admin functionalities:**
  
  - Register and log in.
  - View assignments tagged to the admin.
  - Accept or reject assignments.

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MongoDB
- **Authentication:** Bearer Token Authentication using OAuth2PasswordBearer
- **Asynchronous MongoDB Driver:** Motor

## Installation

1. **Clone the repository**:

    ```bash
        git clone https://github.com/theBatman07/Assignment_Submission_Portal.git
        cd assignment-portal
    ```

2. **Set up a virtual environment** (optional but recommended):

    ```bash
        python -m venv .venv

        .venv\Scripts\activate
    ```

3. **Install the dependencies**:

    ```bash
        pip install -r requirements.txt
    ```

4. **Make a .env file** and add the MONGODB_URL
  
    ```bash
        MONGODB_URL
    ```
  

5. **Run the FastAPI app**:

    ```bash
        uvicorn main:app --reload
    ```

## API Documentation

FastAPI automatically generates interactive API documentation that you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### User Endpoints

1. **Register a user**: `POST /user/register`
  
  **Body**:
  
  ```json
  { 
    "username": "john_doe", 
    "password": "password123",
    "role": "user" 
  }
  ```
  
2. **Login a user**: `POST /user/login`
  
  **Body**:
  
  ```json
  { 
    "username": "john_doe", 
    "password": "password123" 
  }
  ```
  
3. **Upload an assignment**: `POST /user/upload`
  
  **Authorization**: Bearer Token (User login token)
  
  **Body**:
  
  ```json
  { 
      "task": "Complete HelloWorld project", 
      "admin": "admin_username" 
  }
  ```
  
4. **Fetch all admins**: `GET /user/admins`
  
  **Authorization**: Bearer Token (User login token)
  

### Admin Endpoints

1. **Register an admin**: `POST /admin/register`
  
  **Body**:
  
  ```json
  { 
      "username": "admin1", 
      "password": "adminpassword", 
      "role": "admin" 
  }
  ```
  
2. **Login an admin**: `POST /admin/login`
  
  **Body**:
  
  ```json
  { 
      "username": "admin1", 
      "password": "adminpassword" 
  }
  ```
  
3. **View assignments for the admin**: `GET /admin/assignments`
  
  **Authorization**: Bearer Token (Admin login token)
  
4. **Accept an assignment**: `POST /admin/assignments/{id}/accept`
  
  **Authorization**: Bearer Token (Admin login token)
  
5. **Reject an assignment**: `POST /admin/assignments/{id}/reject`
  
  **Authorization**: Bearer Token (Admin login token)