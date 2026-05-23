# AGENTS.md — TravelBudgetPlanner API Spec

Hackathon project. **Keep every implementation as simple as possible.**
No ORM, no database — use in-memory state or flat JSON files.
All routes live in `service/main.py`. All models live in `service/models/`.

---

## Models

All models are Pydantic `BaseModel`. Existing models are in `service/models/travel.py` and `service/models/user.py`. Do not duplicate them.

### User  (`service/models/user.py`)
```python
class User(BaseModel):
    userId: str
    username: str
    passwordHash: str
    firstName: str
    lastName: str
    friendIds: list[str]
    createdAt: datetime
```

### PromptRequestModel  (`service/models/travel.py`)
```python
class PromptRequestModel(BaseModel):
    message: str
```

### PromptResponseModel  (`service/models/travel.py`)
```python
class PromptResponseModel(BaseModel):
    departureDate: str
    returnDate: str
    destinations: list[str]
    activities: list[str]
```

### ActivityDetails  (`service/models/travel.py`)
```python
class ActivityDetails(BaseModel):
    name: str
    price: str
```

### AccommodationDetails  (`service/models/travel.py`)
```python
class AccommodationDetails(BaseModel):
    name: str
    price: str
```

### City  (`service/models/travel.py`)
```python
class City(BaseModel):
    name: str
    country: str
    accommodation: AccommodationDetails
    activityDetails: list[ActivityDetails]
```

### Transportation  (`service/models/travel.py`)
```python
class Transportation(BaseModel):
    departure: str
    arrival: str
    transportationType: TransportationType  # Enum: "Flight" | "Bus" | "Train"
    price: str
```

### Destination  (`service/models/travel.py`)
```python
class Destination(BaseModel):
    name: str
    cities: list[City]
    transportation: list[Transportation]
```

### DestinationPackage  (`service/models/travel.py`)
```python
class DestinationPackage(BaseModel):
    destinationsList: list[Destination]
    destinationName: str
    totalPrice: str
    description: Optional[str] = None
    picture: str
```

### Summary  (`service/models/travel.py`)
```python
class Summary(BaseModel):
    summary: list[DestinationPackage]
```

---

## API Endpoints

All routes are registered on the `app` FastAPI instance in `service/main.py`.

---

### GET /users

Returns the list of all users.

**Response** `200 application/json` — `list[User]`

```json
[
  {
    "userId": "u1",
    "username": "jdoe",
    "passwordHash": "hashed",
    "firstName": "John",
    "lastName": "Doe",
    "friendIds": ["u2"],
    "createdAt": "2024-01-01T00:00:00"
  }
]
```

**Implementation notes:**
- Seed with at least two hardcoded users loaded at startup (in-memory list, same pattern as `transactions`).
- Do not implement auth for the hackathon demo.

---

### POST /prompt

Parses a natural-language travel message and extracts structured trip intent using an LLM (Claude API).

**Request body** — `PromptRequestModel`
```json
{ "message": "I want to visit Paris and Rome for 10 days in July, I love food and museums" }
```

**Response** `200 application/json` — `PromptResponseModel`
```json
{
  "departureDate": "2025-07-01",
  "returnDate": "2025-07-10",
  "destinations": ["Paris", "Rome"],
  "activities": ["food", "museums"]
}
```

**Implementation notes:**
- Call the Anthropic API with a system prompt instructing it to return **only valid JSON** matching `PromptResponseModel`.
- Parse the JSON string from the LLM response and return it as `PromptResponseModel`.
- Use `claude-sonnet-4-6` model.
- Keep the system prompt short and direct — tell the model to return only a JSON object with keys: `departureDate`, `returnDate`, `destinations`, `activities`.

---

### POST /suggestions

Given structured trip intent, return a list of `DestinationPackage` suggestions.

**Request body** — `PromptResponseModel`
```json
{
  "departureDate": "2025-07-01",
  "returnDate": "2025-07-10",
  "destinations": ["Paris", "Rome"],
  "activities": ["food", "museums"]
}
```

**Response** `200 application/json` — `Summary`
```json
{
  "summary": [
    {
      "destinationName": "Paris & Rome Explorer",
      "destinationsList": [...],
      "totalPrice": "$3200",
      "description": "A curated 10-day food and culture trip.",
      "picture": "https://..."
    }
  ]
}
```

**Implementation notes:**
- Call the Anthropic API with the trip intent serialized as context.
- System prompt must instruct the LLM to return **only valid JSON** matching `Summary` (i.e., `{ "summary": [ ...DestinationPackage... ] }`).
- Each `DestinationPackage` must include nested `Destination → City → AccommodationDetails / ActivityDetails` objects.
- Parse and return as `Summary`.
- Use `claude-sonnet-4-6`.

---

### POST /destPackage

Saves a `DestinationPackage` to the in-memory store.

**Request body** — `DestinationPackage`
```json
{
  "destinationName": "Paris & Rome Explorer",
  "destinationsList": [...],
  "totalPrice": "$3200",
  "description": "Optional note",
  "picture": "https://..."
}
```

**Response** `200 application/json`
```json
{ "status": "ok" }
```

**Implementation notes:**
- Append the package to a module-level `dest_packages: list[DestinationPackage] = []` list (same pattern as `transactions`).
- No persistence required.

---

### GET /destPackage

Returns all saved destination packages.

**Response** `200 application/json` — `list[DestinationPackage]`
```json
[
  {
    "destinationName": "Paris & Rome Explorer",
    "destinationsList": [...],
    "totalPrice": "$3200",
    "description": "Optional note",
    "picture": "https://..."
  }
]
```

**Implementation notes:**
- Return the same `dest_packages` list populated by `POST /destPackage`.

---

## Conventions

| Rule | Detail |
|---|---|
| LLM client | `import anthropic; client = anthropic.Anthropic()` (key from env `ANTHROPIC_API_KEY`) |
| LLM model | `claude-sonnet-4-6` |
| JSON parsing | Use `json.loads()` on `response.content[0].text` |
| Error handling | Wrap LLM calls in try/except; return `500` with `{"detail": str(e)}` on failure |
| CORS | Add `CORSMiddleware` with `allow_origins=["*"]` for local frontend dev |
| In-memory state | Module-level lists initialized at startup via `lifespan` |
| No auth | Skip all authentication for the hackathon demo |
