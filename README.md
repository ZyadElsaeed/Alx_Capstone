# Task Management API

A production-ready RESTful API built with **Django** and **Django REST Framework** for managing personal tasks. Supports user registration, token-based authentication, full CRUD operations on tasks, filtering, searching, pagination, and auto-generated Swagger documentation.

---

## Features

- User registration and login with token-based authentication
- Logout endpoint (token deletion)
- Create, read, update, and delete tasks
- Each user can only access their own tasks
- Filter tasks by status (`pending` / `completed`)
- Search tasks by title
- Pagination (10 items per page)
- UUID primary keys for tasks
- Optional due date for tasks
- Swagger / OpenAPI documentation via drf-spectacular
- Custom `IsOwner` permission class
- Root URL (`/`) redirects to Swagger docs automatically
- Clean architecture with separate `config`, `users`, and `tasks` apps

---

## Tech Stack

| Component           | Technology                  |
|---------------------|-----------------------------|
| Language            | Python 3.13+                |
| Framework           | Django 5.1                  |
| API Framework       | Django REST Framework 3.15  |
| Authentication      | DRF Token Authentication    |
| Database (dev)      | SQLite                      |
| Database (prod)     | PostgreSQL                  |
| Filtering           | django-filter               |
| API Docs            | drf-spectacular (Swagger)   |
| Config Management   | python-decouple             |

---

## Project Structure

```
task-management-api/
├── config/              # Django project settings, URLs, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/               # User registration, login, logout
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── tasks/               # Task model, CRUD API, permissions, filters
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── filters.py
│   ├── admin.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/task-management-api.git
cd task-management-api
```

### 2. Create a virtual environment

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

> **Note:** On Windows, if you have multiple Python installations (e.g. MSYS2/MinGW alongside the official CPython), make sure to create the venv with the official CPython executable:
> ```powershell
> & "C:\Users\<you>\AppData\Local\Programs\Python\Python313\python.exe" -m venv venv
> ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For **production with PostgreSQL**, also install:

```bash
pip install psycopg2-binary gunicorn
```

### 4. Configure environment variables

Copy the example file and edit as needed:

**Linux / macOS:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

For development, the defaults (SQLite, debug mode) work out of the box — no `.env` file is required.

For **production**, create a `.env` with:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=taskdb
DB_USER=taskuser
DB_PASSWORD=securepassword
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.
Visiting the root URL automatically redirects to the Swagger documentation.

---

## Environment Variables

| Variable         | Description                          | Default                          |
|------------------|--------------------------------------|----------------------------------|
| `SECRET_KEY`     | Django secret key                    | `django-insecure-dev-key-...`    |
| `DEBUG`          | Debug mode                           | `True`                           |
| `ALLOWED_HOSTS`  | Comma-separated allowed hosts        | `localhost,127.0.0.1`            |
| `DB_ENGINE`      | Database engine                      | `django.db.backends.sqlite3`     |
| `DB_NAME`        | Database name                        | `db.sqlite3`                     |
| `DB_USER`        | Database user                        | (empty)                          |
| `DB_PASSWORD`    | Database password                    | (empty)                          |
| `DB_HOST`        | Database host                        | (empty)                          |
| `DB_PORT`        | Database port                        | (empty)                          |

---

## API Endpoints

### Authentication

| Method | Endpoint          | Description                | Auth Required |
|--------|-------------------|----------------------------|---------------|
| POST   | `/api/register/`  | Register a new user        | No            |
| POST   | `/api/login/`     | Login and receive token    | No            |
| POST   | `/api/logout/`    | Logout (delete token)      | Yes           |

### Tasks

| Method | Endpoint              | Description                  | Auth Required |
|--------|-----------------------|------------------------------|---------------|
| GET    | `/api/tasks/`         | List all tasks (paginated)   | Yes           |
| POST   | `/api/tasks/`         | Create a new task            | Yes           |
| GET    | `/api/tasks/{id}/`    | Retrieve a specific task     | Yes           |
| PUT    | `/api/tasks/{id}/`    | Full update a task           | Yes           |
| PATCH  | `/api/tasks/{id}/`    | Partial update a task        | Yes           |
| DELETE | `/api/tasks/{id}/`    | Delete a task                | Yes           |

### Other

| Method | Endpoint          | Description                          | Auth Required |
|--------|-------------------|--------------------------------------|---------------|
| GET    | `/`               | Redirects to `/api/docs/`            | No            |
| GET    | `/api/docs/`      | Swagger UI                           | No            |
| GET    | `/api/schema/`    | OpenAPI schema (YAML)                | No            |
| GET    | `/admin/`         | Django admin panel                   | Admin         |

### Query Parameters

| Parameter  | Description                              | Example                        |
|------------|------------------------------------------|--------------------------------|
| `status`   | Filter by status                         | `?status=pending`              |
| `search`   | Search by title                          | `?search=groceries`            |
| `ordering` | Order results                            | `?ordering=-created_at`        |
| `page`     | Pagination page number                   | `?page=2`                      |

---

## Example Requests

### Register

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "securepass1", "password_confirm": "securepass1"}'
```

**Response (201 Created):**

```json
{
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "token": "a1b2c3d4e5f6..."
}
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "securepass1"}'
```

**Response (200 OK):**

```json
{
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "token": "a1b2c3d4e5f6..."
}
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "due_date": "2026-03-15"}'
```

**Response (201 Created):**

```json
{
  "id": "a1b2c3d4-...",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "due_date": "2026-03-15",
  "created_at": "2026-03-01T12:00:00Z",
  "updated_at": "2026-03-01T12:00:00Z",
  "user": "john"
}
```

### List Tasks (with filtering)

```bash
curl http://127.0.0.1:8000/api/tasks/?status=pending \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Update a Task

```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/TASK_UUID/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a Task

```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/TASK_UUID/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Logout

```bash
curl -X POST http://127.0.0.1:8000/api/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Swagger Documentation

Once the server is running, visit:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

Or simply open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — it redirects to the Swagger UI automatically.

---

## Running Tests

Run the full test suite (15 tests):

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test users
python manage.py test tasks
```

Run with verbose output:

```bash
python manage.py test --verbosity=2
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).
