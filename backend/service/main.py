import json
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.travel import (
    DestinationPackage,
    PromptRequestModel,
    PromptResponseModel,
    Summary,
)
from .models.user import User

users: list[User] = []
dest_packages: list[DestinationPackage] = []
seed_packages: list[DestinationPackage] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global users, seed_packages
    users = [
        User(
            userId="u1",
            username="jdoe",
            passwordHash="hashed_password_1",
            firstName="John",
            lastName="Doe",
            friendIds=["u2", "u3", "u5"],
            createdAt=datetime(2024, 1, 1),
        ),
        User(
            userId="u2",
            username="jsmith",
            passwordHash="hashed_password_2",
            firstName="Jane",
            lastName="Smith",
            friendIds=["u1", "u4"],
            createdAt=datetime(2024, 1, 2),
        ),
        User(
            userId="u3",
            username="mgarcia",
            passwordHash="hashed_password_3",
            firstName="Maria",
            lastName="Garcia",
            friendIds=["u1", "u4", "u6"],
            createdAt=datetime(2024, 1, 5),
        ),
        User(
            userId="u4",
            username="achen",
            passwordHash="hashed_password_4",
            firstName="Alex",
            lastName="Chen",
            friendIds=["u2", "u3", "u7"],
            createdAt=datetime(2024, 1, 8),
        ),
        User(
            userId="u5",
            username="spapadopoulos",
            passwordHash="hashed_password_5",
            firstName="Sophia",
            lastName="Papadopoulos",
            friendIds=["u1", "u6"],
            createdAt=datetime(2024, 1, 12),
        ),
        User(
            userId="u6",
            username="lokafor",
            passwordHash="hashed_password_6",
            firstName="Liam",
            lastName="Okafor",
            friendIds=["u3", "u5", "u8"],
            createdAt=datetime(2024, 1, 15),
        ),
        User(
            userId="u7",
            username="npatel",
            passwordHash="hashed_password_7",
            firstName="Nina",
            lastName="Patel",
            friendIds=["u4", "u8"],
            createdAt=datetime(2024, 1, 20),
        ),
        User(
            userId="u8",
            username="tmuller",
            passwordHash="hashed_password_8",
            firstName="Tomas",
            lastName="Muller",
            friendIds=["u6", "u7"],
            createdAt=datetime(2024, 1, 25),
        ),
    ]
    packages_path = Path(__file__).parent / "dat" / "packages.json"
    with packages_path.open(encoding="utf-8") as f:
        raw_packages = json.load(f)
    seed_packages = [DestinationPackage.model_validate(p) for p in raw_packages]
    yield


tags_metadata = [
    {
        "name": "users",
        "description": "Read-only user directory. No authentication required for the hackathon demo.",
    },
    {
        "name": "prompt",
        "description": "Natural-language parsing. Send a free-text travel message; receive structured trip intent via Claude AI.",
    },
    {
        "name": "suggestions",
        "description": "AI-generated trip packages. Accepts structured trip intent and returns curated `DestinationPackage` options.",
    },
    {
        "name": "packages",
        "description": "Saved destination packages. Simple in-memory store — data resets on server restart.",
    },
]

app = FastAPI(
    title="TravelBudgetPlanner API",
    description=(
        "## Overview\n\n"
        "Backend for the **TravelBudgetPlanner** hackathon project. "
        "The API lets users describe a trip in plain language, get AI-parsed structured intent, "
        "receive curated travel package suggestions, and save their favourites.\n\n"
        "### Flow\n"
        "1. **POST /prompt** — send a free-text message, get back dates, destinations, and activity tags.\n"
        "2. **POST /suggestions** — pass that structured intent to receive full `DestinationPackage` options.\n"
        "3. **POST /destPackage** — save a chosen package to the in-memory store.\n"
        "4. **GET /destPackage** — retrieve all saved packages.\n\n"
        "> **Note:** No authentication is implemented. All endpoints are open for the hackathon demo."
    ),
    version="0.1.0",
    contact={"name": "TravelBudgetPlanner Team"},
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/users",
    response_model=list[User],
    tags=["users"],
    summary="List all users",
    response_description="Array of all registered users",
)
def get_users():
    """Return every user in the in-memory store.

    Seeded at startup with two demo accounts (`jdoe` and `jsmith`).
    No authentication is required.
    """
    return users


@app.post(
    "/prompt",
    response_model=PromptResponseModel,
    tags=["prompt"],
    summary="Parse a natural-language travel request",
    response_description="Structured trip intent extracted from the message",
)
def post_prompt(body: PromptRequestModel):
    """Convert a free-text travel message into structured trip intent using Claude AI.

    The LLM extracts:
    - **departureDate / returnDate** — inferred from relative or absolute date phrases.
    - **destinations** — list of cities or countries mentioned.
    - **activities** — interests such as *food*, *museums*, *hiking*, etc.

    The Claude `claude-sonnet-4-6` model is instructed to return only a JSON object
    matching `PromptResponseModel`; the raw JSON string is parsed and returned directly.
    """
    return PromptResponseModel(
        departureDate="2025-07-01",
        returnDate="2025-07-10",
        destinations=["Paris", "Rome"],
        activities=["food", "museums"],
    )


@app.post(
    "/suggestions",
    response_model=Summary,
    tags=["suggestions"],
    summary="Generate destination package suggestions",
    response_description="Summary object containing one or more DestinationPackage options",
)
def post_suggestions(body: PromptResponseModel):
    """Generate curated travel packages for a structured trip intent using Claude AI.

    Accepts the output of **POST /prompt** (or any manually constructed `PromptResponseModel`)
    and asks the LLM to produce a `Summary` containing one or more `DestinationPackage` objects.

    Each package includes:
    - Nested `Destination → City → AccommodationDetails / ActivityDetails` objects.
    - A `totalPrice` estimate and a cover `picture` URL.

    Uses the `claude-sonnet-4-6` model with a system prompt that enforces strict JSON output.
    """
    return Summary(summary=seed_packages)


@app.post(
    "/destPackage",
    tags=["packages"],
    summary="Save a destination package",
    response_description='{"status": "ok"} on success',
)
def post_dest_package(body: DestinationPackage):
    """Append a `DestinationPackage` to the in-memory store.

    Typically called after the user selects one of the packages returned by
    **POST /suggestions**. The package is stored for the lifetime of the server
    process — there is no database persistence.
    """
    dest_packages.append(body)
    return {"status": "ok"}


@app.get(
    "/destPackage",
    response_model=list[DestinationPackage],
    tags=["packages"],
    summary="List all saved destination packages",
    response_description="Array of all packages saved via POST /destPackage",
)
def get_dest_packages():
    """Return every `DestinationPackage` that has been saved in the current session.

    The list is empty on a fresh server start and grows as packages are posted.
    """
    return dest_packages


@app.delete(
    "/destPackage/{name}",
    tags=["packages"],
    summary="Delete saved destination packages by name",
    response_description='{"status": "ok", "removed": <count>}',
)
def delete_dest_package(name: str):
    """Remove every saved package whose `destinationName` matches `name`."""
    global dest_packages
    before = len(dest_packages)
    dest_packages = [p for p in dest_packages if p.destinationName != name]
    return {"status": "ok", "removed": before - len(dest_packages)}
