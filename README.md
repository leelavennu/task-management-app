# Task Management Web Application

## Tech Stack
Python Flask, React TypeScript, PostgreSQL, Pytest, Jest, Docker, SQLAlchemy, Pydantic, Tailwind CSS

## Features
CRUD, validation, auth, responsive accessible UI

- Task board with add, edit, complete/uncomplete, delete, and completed filtering
- Bearer token authentication on every `/api/tasks` endpoint
- PostgreSQL production configuration with SQLite fallback for local development
- Accessible labels, ARIA labels, focus states, keyboard-friendly buttons, and mobile layout
- Loading skeletons, empty state, network failure banner, unauthorized message, retry action

## Setup
```bash
Backend
cd backend
pip install -r requirements.txt
python app.py

Frontend
cd frontend
npm install
npm run dev

Docker
docker-compose up
```

## API Behavior
All endpoints require `Authorization: Bearer test-token`.

| Method | Endpoint | Behavior |
|---|---|---|
| POST | `/api/tasks` | Creates a task. Requires `title`; accepts `description`, ISO-8601 `due_date`, and `completed`. Returns `201`. |
| GET | `/api/tasks` | Lists tasks. Optional `completed=true|false` filter. Malformed query values return `400`. |
| GET | `/api/tasks/{id}` | Returns one task or `404`. |
| PUT | `/api/tasks/{id}` | Replaces task fields and returns the updated task. |
| DELETE | `/api/tasks/{id}` | Deletes a task and returns `204`. |

Example:
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H 'Authorization: Bearer test-token' -H 'Content-Type: application/json' \
  -d '{"title":"Review pull request","description":"Check tests","due_date":"2030-01-01T10:00:00Z"}'
```

## Edge Cases Tested
- malformed requests (invalid JSON) -> `400`
- network failures -> UI error banner
- invalid input -> form error messages and `400` API responses
- authorization -> missing or invalid token returns `401`
- empty states -> “No tasks yet - create your first task” placeholder UI
- server errors -> retry UI
- invalid due dates -> past dates and wrong formats return `400`
- special characters are stored as text and rendered safely by React
- unknown task IDs return `404`

## Known Limitations
- Simple token auth, not JWT
- PostgreSQL required for production, SQLite for dev
- No pagination yet (intentional difference from Project 1)

## Testing Instructions
```bash
cd backend
pytest

cd ../frontend
npm install
npm test
```
