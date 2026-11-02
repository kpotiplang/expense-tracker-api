# Expense Tracker API

A RESTful API built with Flask and SQLite that lets users create, read, update, and delete expenses.

## Features
- Full CRUD for expenses
- Persistent storage with SQLite (via Flask-SQLAlchemy)
- JSON request and response bodies
- Input validation with clear `400` errors for bad requests
- Automated tests with pytest

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/expenses` | List all expenses |
| GET | `/expenses/<id>` | Get one expense |
| POST | `/expenses` | Create an expense (`title` and `amount` required) |
| PUT | `/expenses/<id>` | Update any fields of an expense |
| DELETE | `/expenses/<id>` | Delete an expense |

## Example request

```bash
curl -X POST http://localhost:5000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Rent", "amount": 1200, "category": "Housing", "date": "2026-11-01"}'
```

Response (`201 Created`):

```json
{
  "id": 1,
  "title": "Rent",
  "amount": 1200,
  "category": "Housing",
  "date": "2026-11-01"
}
```

Invalid input returns `400`:

```json
{ "error": "Missing required field: amount" }
```

## Run it locally

```bash
pip install -r requirements.txt
python app.py
```

The server runs on port 5000 by default, or on the port in the `PORT` environment variable.

## Run the tests

```bash
pytest
```

The tests use an in-memory database, so they don't touch your local data.

## Tech stack
- Python
- Flask
- Flask-SQLAlchemy / SQLite
- pytest

## What I'd improve next
- Store amounts as integer cents (or `Decimal`) instead of a float, to avoid rounding errors with money
- Add user accounts and authentication so each user only sees their own expenses
- Add pagination and filtering (e.g. `?category=Food&limit=20`) to `GET /expenses`
- Store `date` as a real date column instead of a string
