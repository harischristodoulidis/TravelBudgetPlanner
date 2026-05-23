import json
import logging
import os
import re
from contextlib import asynccontextmanager

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")
from datetime import datetime, date

import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

from .models.travel import (
    AccommodationDetails,
    ActivityDetails,
    City,
    Destination,
    DestinationPackage,
    PromptRequestModel,
    PromptResponseModel,
    Summary,
    Transportation,
    TransportationType,
)
from .models.user import User

users: list[User] = []
dest_packages: list[DestinationPackage] = []


def _guard_dates(data: dict) -> list[str]:
    """Returns a list of date issues. Empty list means all good."""
    issues = []
    today = date.today()
    for field in ("departureDate", "returnDate"):
        raw = data.get(field, "")
        if not raw:
            issues.append(f"{field} is missing")
            continue
        try:
            parsed = date.fromisoformat(raw[:10])
        except ValueError:
            issues.append(f"{field} '{raw}' is not a valid date")
            continue
        if parsed <= today:
            issues.append(f"{field} '{raw}' must be a future date")

    if not issues:
        dep = date.fromisoformat(data["departureDate"][:10])
        ret = date.fromisoformat(data["returnDate"][:10])
        if dep >= ret:
            issues.append("departureDate must be before returnDate")

    return issues


def _correct_dates(data: dict, issues: list[str], original_message: str, model: genai.GenerativeModel) -> None:
    """Ask the LLM to correct invalid dates in-place."""
    prompt = (
        f"A trip intent was parsed from this message: '{original_message}'\n"
        f"The following date problems were found: {issues}\n"
        f"Current values: departureDate={data.get('departureDate')}, returnDate={data.get('returnDate')}\n"
        f"Today is {date.today().isoformat()}. Infer sensible future dates from the original message context.\n"
        "Return ONLY a JSON object with departureDate and returnDate as YYYY-MM-DD strings. No markdown, no explanation."
    )
    response = model.generate_content(prompt)
    raw = response.text.strip()
    logger.debug("Date correction raw response: %r", raw)
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not match:
        logger.warning("Date correction returned unparseable response")
        return
    corrected = json.loads(match.group())
    for field in ("departureDate", "returnDate"):
        if field in corrected:
            data[field] = corrected[field]
            logger.info("Date corrected: %s → %s", field, corrected[field])


def _guard_destinations(destinations: list[str], model: genai.GenerativeModel) -> None:
    if not destinations:
        raise HTTPException(status_code=422, detail="No destinations were found in your message")

    prompt = (
        f"Are these valid, real-world travel destinations? {destinations}\n"
        "Return ONLY a JSON object with exactly two fields: "
        "valid (boolean, true if ALL are real places), invalid (array of strings that are NOT real destinations). "
        "No markdown, no explanation."
    )
    response = model.generate_content(prompt)
    raw = response.text.strip()
    logger.debug("Destination guard raw response: %r", raw)

    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if not match:
        logger.warning("Destination guard returned unparseable response — skipping")
        return

    result = json.loads(match.group())
    if not result.get("valid", True):
        invalid = result.get("invalid", [])
        raise HTTPException(status_code=422, detail=f"These destinations don't appear to be real places: {invalid}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup: seeding in-memory user store")
    global users
    users = [
        User(
            userId="u1",
            username="jdoe",
            passwordHash="hashed_password_1",
            firstName="John",
            lastName="Doe",
            friendIds=["u2"],
            createdAt=datetime(2024, 1, 1),
        ),
        User(
            userId="u2",
            username="jsmith",
            passwordHash="hashed_password_2",
            firstName="Jane",
            lastName="Smith",
            friendIds=["u1"],
            createdAt=datetime(2024, 1, 2),
        ),
    ]
    logger.info("Startup complete: %d users loaded", len(users))
    yield
    logger.info("Shutdown: application lifespan ending")


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
    logger.info("GET /users: returning %d users", len(users))
    return users


@app.post(
    "/prompt",
    response_model=PromptResponseModel,
    tags=["prompt"],
    summary="Parse a natural-language travel request",
    response_description="Structured trip intent extracted from the message",
)
def post_prompt(body: PromptRequestModel):
    """Convert a free-text travel message into structured trip intent using Gemini.

    The LLM extracts:
    - **departureDate / returnDate** — inferred from relative or absolute date phrases.
    - **destinations** — list of cities or countries mentioned.
    - **activities** — interests such as *food*, *museums*, *hiking*, etc.

    Required env var:
    - GEMINI_API_KEY — Google AI Studio API key (free tier available)

    Optional env var:
    - GEMINI_MODEL (defaults to gemini-2.0-flash)
    """
    logger.info("POST /prompt: received message: %r", body.message)
    try:
        api_key = os.getenv("GEMINI_API_KEY", "")
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set")
        logger.debug("Gemini config: model=%s", model_name)

        prompt = (
            "Extract trip details from the following travel message and return ONLY a valid JSON object "
            "with these exact fields: departureDate (ISO-8601 string), returnDate (ISO-8601 string), "
            "destinations (array of strings), activities (array of strings). "
            f"No markdown, no explanation — just the JSON object.\n\nMessage: {body.message}"
        )

        logger.info("Calling Gemini API")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        raw = response.text
        logger.debug("Gemini raw response repr: %r", raw)

        if not raw or not raw.strip():
            logger.error("Gemini returned an empty response")
            raise HTTPException(status_code=502, detail="Gemini returned an empty response")

        data: dict | None = None
        stripped = raw.strip()
        if stripped.startswith("{"):
            try:
                data = json.loads(stripped)
                logger.debug("Parsed JSON directly from raw response")
            except json.JSONDecodeError:
                logger.debug("Direct parse failed, falling back to regex extraction")

        if data is None:
            logger.info("Extracting JSON object from AI response via regex")
            match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
            if not match:
                logger.error("No JSON object found in AI response: %r", raw)
                raise HTTPException(status_code=502, detail=f"No JSON object found in AI response: {raw}")
            matched_str = match.group().strip()
            logger.debug("Regex-matched string repr: %r", matched_str)
            data = json.loads(matched_str)

        data["destinations"] = data.get("destinations") or []
        data["activities"] = data.get("activities") or []

        iso_date_re = re.compile(r"\d{4}-\d{2}-\d{2}(?:T[\d:]+Z?)?")
        for field in ("departureDate", "returnDate"):
            raw_date = data.get(field) or ""
            m = iso_date_re.search(str(raw_date))
            data[field] = m.group() if m else ""

        logger.info("Successfully parsed trip intent: destinations=%s activities=%s", data["destinations"], data["activities"])

        date_issues = _guard_dates(data)
        if date_issues:
            logger.warning("Date issues detected: %s — attempting LLM correction", date_issues)
            _correct_dates(data, date_issues, body.message, model)
            date_issues = _guard_dates(data)
            if date_issues:
                raise HTTPException(status_code=422, detail=f"Could not produce valid dates: {date_issues}")

        _guard_destinations(data["destinations"], model)

        return PromptResponseModel(**data)

    except json.JSONDecodeError as e:
        logger.error("LLM returned invalid JSON: %s", e)
        raise HTTPException(status_code=502, detail=f"LLM returned invalid JSON: {e}")
    except Exception as e:
        logger.error("Gemini API error: %s", e)
        raise HTTPException(status_code=502, detail=f"Gemini API error: {e}")


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
    logger.info(
        "POST /suggestions: generating packages for destinations=%s activities=%s departure=%s return=%s",
        body.destinations, body.activities, body.departureDate, body.returnDate,
    )
    logger.debug("Building mock destination package")
    mock_package = DestinationPackage(
        destinationName="Paris & Rome Explorer",
        totalPrice="$3200",
        description="A curated 10-day food and culture trip through Paris and Rome.",
        picture="https://images.unsplash.com/photo-1499856871958-5b9627545d1a",
        destinationsList=[
            Destination(
                name="Paris",
                cities=[
                    City(
                        name="Paris",
                        country="France",
                        accommodation=AccommodationDetails(name="Hotel Le Marais", price="$150/night"),
                        activityDetails=[
                            ActivityDetails(name="Louvre Museum", price="$20"),
                            ActivityDetails(name="Eiffel Tower", price="$30"),
                            ActivityDetails(name="French Cooking Class", price="$80"),
                        ],
                    )
                ],
                transportation=[
                    Transportation(
                        departure="New York JFK",
                        arrival="Paris CDG",
                        transportationType=TransportationType.flight,
                        price="$650",
                    )
                ],
            ),
            Destination(
                name="Rome",
                cities=[
                    City(
                        name="Rome",
                        country="Italy",
                        accommodation=AccommodationDetails(name="Hotel Colosseo", price="$130/night"),
                        activityDetails=[
                            ActivityDetails(name="Colosseum Tour", price="$25"),
                            ActivityDetails(name="Vatican Museums", price="$35"),
                            ActivityDetails(name="Italian Food Tour", price="$60"),
                        ],
                    )
                ],
                transportation=[
                    Transportation(
                        departure="Paris CDG",
                        arrival="Rome FCO",
                        transportationType=TransportationType.flight,
                        price="$180",
                    )
                ],
            ),
        ],
    )
    logger.info("POST /suggestions: returning 1 package: %s", mock_package.destinationName)
    return Summary(summary=[mock_package])


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
    logger.info("POST /destPackage: saving package %r", body.destinationName)
    dest_packages.append(body)
    logger.info("POST /destPackage: store now has %d packages", len(dest_packages))
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
    logger.info("GET /destPackage: returning %d packages", len(dest_packages))
    return dest_packages
