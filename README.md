# TravelBudgetPlanner

## Backend

### Prerequisites

- Python 3.11+

### Setup

```bash
cd backend
pip install -r requirements.txt
```

### Run the dev server

```bash
# from the backend/ directory
uvicorn service.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/users` | List all users |
| `POST` | `/prompt` | Parse a free-text travel request into structured intent |
| `POST` | `/suggestions` | Generate destination package suggestions from structured intent |
| `POST` | `/destPackage` | Save a chosen destination package |
| `GET` | `/destPackage` | List all saved destination packages |

### Project layout

```
backend/
├── service/
│   ├── main.py          # FastAPI app and all routes
│   ├── data.py          # Data loading logic
│   ├── travel_data.py
│   ├── models/          # Pydantic schemas
│   │   ├── travel.py
│   │   ├── transaction.py
│   │   └── user.py
│   └── dat/
│       └── packages.json
├── worker/              # Background worker
├── typescript/          # Shared TypeScript type definitions
├── specs/               # Backend-specific specs
├── user_transaction_data.csv
└── requirements.txt
```