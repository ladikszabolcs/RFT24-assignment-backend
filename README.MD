
# UniCourse Backend

This is the backend for the UniCourse lecture management software, built with Django and Django REST Framework. It provides a REST API for managing users, lectures, and lecture enrollments.

## Features
- User management with three roles: Admin, Teacher, and Student.
- Lecture management (create, read, update, delete lectures).
- Lecture enrollment for students.
- Token-based authentication using `rest_framework.authtoken`.

## Live Demo
- **Backend API**: [https://unicourse-backend.onrender.com/](https://unicourse-backend.onrender.com/)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ladikszabolcs/RFT24-assignment-backend.git
   cd RFT24-assignment-backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create an api user:
   ```bash
   python manage.py create_api_user <username> <password> <email> <role>
      ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Authentication
This API uses token-based authentication. Obtain a token by sending a POST request to `/auth/token/` with valid credentials.

## API Endpoints

### Authentication
| Method | Endpoint        | Description                                         |
|--------|-----------------|-----------------------------------------------------|
| POST   | `/auth/token/`  | Obtain a token for authentication.                 |
| GET    | `/auth/me/`     | Retrieve the current user's details.               |

---

### User Management
| Method | Endpoint        | Description                                         |
|--------|-----------------|-----------------------------------------------------|
| GET    | `/api/users/`   | List all users (admin only).                        |
| POST   | `/api/users/`   | Create a new user (admin only).                     |
| GET    | `/api/users/<id>/` | Retrieve details of a specific user (admin only). |
| PUT    | `/api/users/<id>/` | Update a specific user (admin only).              |
| DELETE | `/api/users/<id>/` | Delete a specific user (admin only).              |

---

### Lecture Management
| Method | Endpoint             | Description                                   |
|--------|----------------------|-----------------------------------------------|
| GET    | `/api/lectures/`     | List all lectures.                           |
| POST   | `/api/lectures/`     | Create a new lecture (admin or teacher).     |
| GET    | `/api/lectures/<id>/`| Retrieve details of a specific lecture.      |
| PUT    | `/api/lectures/<id>/`| Update a specific lecture (admin or teacher).|
| DELETE | `/api/lectures/<id>/`| Delete a specific lecture (admin or teacher).|

---

### Lecture Enrollment
| Method | Endpoint                        | Description                                      |
|--------|---------------------------------|--------------------------------------------------|
| POST   | `/api/lectures/<id>/enroll/`    | Enroll the current student in a lecture.        |
| POST   | `/api/lectures/<id>/unenroll/`  | Unenroll the current student from a lecture.    |

---

## Notes
- Ensure the administrator user is not accidentally deleted, as this could lock you out of administrative features.
- The frontend and backend communicate via REST API, with the frontend consuming the endpoints listed above.

---

## Contributing
Feel free to open an issue or submit a pull request if you'd like to contribute to this project.

---

