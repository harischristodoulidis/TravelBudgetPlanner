# CLAUDE.md

Read PROBLEM.md for the full problem statement and business context.
Read ARCHITECTURE.md for the screen-by-screen UX flow.
The file `wireframe.png` in the repo root is the designer's reference — match it faithfully.

## App identity

- **Name**: BudgetTrip Planner

## Tech stack

- **Frontend**: React + TypeScript (Vite)
- **Styling**: Tailwind CSS (or CSS modules — TBD)
- **State**: React Context or Zustand (make it as simple as possible)
- **Routing**: React Router

## Screens (match wireframe exactly)

### Screen 1 — Plan (`/`)

- `+ Add people` button (blue pill) at top → opens contacts picker
- Free-text `<textarea>` for trip prompt (no character limit)
- Send button (small blue circle) bottom-right of textarea
- People list below textarea as radio-button pills (name + toggle)

### Screen 2 — Destination results (`/results`)

- AI confirmation bubble at top (grey/blue tinted card) summarising what it understood
- Destination cards below: yellow image placeholder | name | theme tag | price per person
- Cards are tappable → navigate to Screen 3
- Show 3 cards; "expand more" below (per ARCHITECTURE.md)

### Screen 3 — Itinerary (`/trip/:id`)

- City name as large heading, theme subtitle below
- Vertical list of line items: diamond icon ◇ | item name (bold) + provider (small muted) | cost right-aligned
- Items cover: flights, transfers, accommodation, activities in chronological order
- `TOTAL € X` pill (blue, rounded) pinned at the bottom
- Accept button leads to Screen 4

### Screen 4 — Vault (`/vault`)

- Toggle card: "Do you want to open a Vault?"
- Goal box: "Goal [X] € each" (bold bordered box)
- Member contribution table: Name | Amount saved so far (color-coded by contribution level)
- Total row at bottom of table
- "X € To the goal" box below (remaining amount)

## Domain concepts

- **Group** — the travellers; each has a financial profile + preference profile from the bank
- **Destination match** — ranked by group budget fit + preference alignment
- **Itinerary** — ordered list of bookable items (flights, transfers, hotels, activities) with provider and cost
- **Vault** — shared savings account; members contribute at their own pace toward the trip total
- **Per-person cost** — all prices shown per person unless labelled otherwise

## Data model hints (from wireframe)

```ts
interface TripItem {
  id: string;
  name: string; // e.g. "Athens – Rome"
  provider: string; // e.g. "Flight Aegean"
  costPerPerson: number;
  category: "flight" | "transfer" | "accommodation" | "activity";
}

interface Destination {
  id: string;
  city: string;
  theme: string; // e.g. "Theatre and night life"
  totalPerPerson: number;
  imageUrl?: string; // yellow placeholder until real images
  items: TripItem[];
}

interface VaultMember {
  name: string;
  saved: number;
  goal: number; // their share of the trip total
}
```

## Common commands

```bash
npm run dev        # Vite dev server
npm run build      # production build
npm run lint       # ESLint
npm run typecheck  # tsc --noEmit
npm test           # Vitest
```

## Code conventions

- Strict TypeScript — no `any`
- Functional components only
- File structure: `src/screens/`, `src/components/`, `src/types/`, `src/hooks/`, `src/services/`
- One component per file, PascalCase filenames
- Props interfaces co-located with component
- API/mock calls live in `src/services/` only

## Warnings

- All prices are **per person** — never show a total without labelling it clearly
- The AI summary bubble (Screen 2) text comes from the backend — do not hardcode it
- Vault contribution amounts are color-coded: high contributor = orange, medium = gold, low = default
- Image placeholders are yellow (`#F5D87A`) until real photos are integrated
- "Match %" logic is backend-owned — frontend only renders what the API returns
- Vault feature should be behind a feature flag until bank API is integrated
