# TravelBudgetPlanner

> _"Plan a trip with your friends based on what you can actually afford."_

A group-travel planner that turns free-text trip ideas (_"long weekend in Italy, museums + food, mid budget"_) into ranked destination packages personalised to the group's bank-transaction history, and lets everyone save toward the trip in a shared vault.

Built as a hackathon project for a bank: the bank supplies each member's spending profile, and in return gets a reason for people to open a joint savings account.

## Why it exists

- Groups struggle to agree on a trip that fits everyone's budget and interests.
- Banks already know how each person spends — that signal is usually locked away.
- Combining the two lets the app suggest places the group can realistically afford **and** will enjoy, then nudge them to save for it together.

See [`UI/specs/PROBLEM.md`](./UI/specs/PROBLEM.md) for the full product framing and [`UI/specs/ARCHITECTURE.md`](./UI/specs/ARCHITECTURE.md) for the screen-by-screen UX.

## How it works

```
free-text message
      │
      ▼
┌──────────────┐    POST /prompt     ┌─────────────────┐
│  React UI    │ ───────────────────▶│  FastAPI        │
│  (Vite)      │                     │  service        │
└──────────────┘ ◀───────────────────│                 │
      │          structured intent   └─────────────────┘
      │                                       │
      │  POST /suggestions                    │ Gemini
      ▼                                       ▼
┌──────────────────┐                 ┌─────────────────┐
│  Destination     │ ◀───────────────│  package.json   │
│  cards + Vault   │                 │  (claudio       │
│                  │                 │   worker)       │
└──────────────────┘                 └─────────────────┘
```

1. **UI** collects friends + a free-text trip prompt (`Plan` screen).
2. **Backend `POST /prompt`** calls Google Gemini to extract `departureDate`, `returnDate`, `destinations`, `activities` from the message, with guard passes for invalid dates and non-real places.
3. **Backend `POST /suggestions`** loads a pre-built package (produced offline by the **claudio** worker — see below) and asks Gemini to pick the destinations in it that best match the user's request.
4. The UI shows ranked destination cards. Tapping one opens the full itinerary (flights, transfers, accommodation, activities with per-person costs).
5. On accept, the user can open a **Vault** — a shared savings account with a per-person goal and contribution tracking.

Full sequence diagram with error / fallback paths: [`SEQUENCE_DIAGRAM.md`](./SEQUENCE_DIAGRAM.md).

### The claudio worker (offline)

`backend/worker/claudio/` runs **before** the API serves traffic and produces `backend/worker/claudio/output/package.json`:

- `generate_accomodation.py`, `generate_transport.py`, `generate_activities.py` build the catalogue (3 properties × 3 cities, flights/trains/buses, 4 activities × 3 cities).
- `user_profiler_scikitlearn.py` ingests the user's Greek-language bank transactions (`user_transaction_data.csv`) via scikit-learn NLP (Naive Bayes) and scores the user 1–10 on **budget**, **cultural**, **nightlife**, **mobility**, **activity**.
- `city_profiler_teleport.py` fetches city scores (budget_city, cultural_city, nightlife_city) from the Teleport API for Rome, Florence, Venice, Athens.
- `destination_criteria.py` ranks cities by Euclidean distance between the user affinity vector and the city profile.

If `package.json` is missing when a client calls `/suggestions`, the API returns **503** with a hint to run the worker first.

## Screens

| Route         | Purpose                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------- |
| `/`           | **Plan** — add friends, free-text prompt, send.                                           |
| `/results`    | **Destinations** — AI summary bubble + ranked destination cards (top 3, then expand).     |
| `/trip/:id`   | **Trip Details** — chronological line items with per-person costs, `TOTAL €` pill at bottom. |
| `/vault`      | **Vault** — open shared savings, per-member goal, contribution table, remaining balance.  |

All prices are **per person** unless explicitly labelled otherwise.

## Repo layout

```
TravelBudgetPlanner/
├── UI/                           React + TypeScript (Vite) frontend
│   ├── src/
│   │   ├── screens/              PlanScreen, TripDetailsScreen, …
│   │   ├── components/           AddPeopleButton, DestinationCard, …
│   │   ├── context/              SessionContext, TripContext, PlannedTripsContext
│   │   ├── services/             API calls (api.ts, session.ts)
│   │   ├── types/
│   │   └── utils/
│   ├── specs/                    Product spec, architecture, wireframe
│   └── package.json
├── backend/
│   ├── service/                  FastAPI app
│   │   ├── main.py               Routes + Gemini integration
│   │   ├── data.py / travel_data.py
│   │   ├── models/               Pydantic schemas (travel, user, transaction)
│   │   └── dat/packages.json
│   ├── worker/
│   │   ├── worker.py             Heartbeat worker
│   │   └── claudio/              Offline personalisation pipeline
│   │       ├── main.py
│   │       ├── generate_*.py     Catalogue builders
│   │       ├── user_profiler_scikitlearn.py
│   │       ├── city_profiler_teleport.py
│   │       ├── destination_criteria.py
│   │       └── output/package.json  ← consumed by /suggestions
│   ├── user_transaction_data.csv
│   └── requirements.txt
└── SEQUENCE_DIAGRAM.md
```

## Tech stack

| Layer | Choice |
| --- | --- |
| Frontend | React 19 + TypeScript (strict), Vite 6, Tailwind CSS v4, React Router 7, Lucide icons |
| Frontend state | React Context (`SessionContext`, `TripContext`, `PlannedTripsContext`) |
| Backend | FastAPI, Uvicorn, Pydantic |
| LLM | Google Gemini (`gemini-2.0-flash` by default) via `google-generativeai` |
| Personalisation | scikit-learn (NLP / Naive Bayes), Teleport API |
| Persistence | **In-memory** — data resets on backend restart (hackathon simplification) |

## Getting started

### Prerequisites

- Node.js 20+
- Python 3.11+
- A Google AI Studio key (`GEMINI_API_KEY`) — free tier works.

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# Create backend/.env with:
#   GEMINI_API_KEY=your_key_here
#   GEMINI_MODEL=gemini-2.0-flash   # optional

# (optional, but required for /suggestions)
cd worker/claudio && python ./main.py && cd ../..

# Run the API
python -m uvicorn service.main:app --reload
```

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>

### 2. Frontend

```bash
cd UI
npm install
npm run dev        # Vite dev server, defaults to http://localhost:5173
```

Other UI scripts:

```bash
npm run build      # tsc -b && vite build
npm run preview    # serve the production build
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
```

### 3. Heartbeat worker (optional)

```bash
cd backend
python worker/worker.py
```

## API reference

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/users` | List all users (seeded in-memory). |
| `POST` | `/prompt` | Parse a free-text travel message into structured intent via Gemini. Includes date-correction and destination-validation guards. |
| `POST` | `/suggestions` | Pick matching destinations from the pre-built claudio package and return as `Summary`. |
| `POST` | `/destPackage` | Save a chosen `DestinationPackage` to the in-memory store. |
| `GET` | `/destPackage` | List all saved packages. |
| `DELETE` | `/destPackage/{name}` | Remove saved packages by `destinationName`. |

### Environment variables

| Var | Where | Required | Default |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | `backend/.env` | yes | — |
| `GEMINI_MODEL` | `backend/.env` | no | `gemini-2.0-flash` |

## Core domain

```ts
interface TripItem {
  id: string;
  name: string;              // "Athens – Rome"
  provider: string;          // "Flight Aegean"
  costPerPerson: number;
  category: "flight" | "transfer" | "accommodation" | "activity";
}

interface Destination {
  id: string;
  city: string;
  theme: string;             // "Theatre and night life"
  totalPerPerson: number;
  imageUrl?: string;
  items: TripItem[];
}

interface VaultMember {
  name: string;
  saved: number;
  goal: number;              // their share of the trip total
}
```

- **Group** — travellers with bank-sourced financial + preference profiles.
- **Destination match** — ranked by budget fit and preference alignment (claudio).
- **Trip Details** — chronological bookable items with provider and cost.
- **Vault** — shared account; members contribute at their own pace.

## Project status & caveats

- Hackathon scope: **no auth, no DB** — users and saved packages are in-memory and reset on restart.
- The `/suggestions` endpoint depends on `backend/worker/claudio/output/package.json`; run the claudio pipeline before hitting that route.
- Gemini calls can fail; the backend has regex JSON-extraction and selection fallbacks (full matrix in `SEQUENCE_DIAGRAM.md`).
- Image placeholders in the UI are yellow (`#F5D87A`) until real photos are integrated.
- The Vault feature is intended to sit behind a feature flag until a real bank API is wired up.
