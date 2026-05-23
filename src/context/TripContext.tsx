import {
  createContext,
  useContext,
  useMemo,
  useReducer,
  type ReactNode,
} from "react";
import type { MatchResponse, Person } from "../types/trip";
import { useSession } from "./SessionContext";

interface TripState {
  people: Person[];
  selectedPersonIds: string[];
  prompt: string;
  lastResults: MatchResponse | null;
}

type TripAction =
  | { type: "addPeople"; people: Person[] }
  | { type: "togglePerson"; id: string }
  | { type: "removePerson"; id: string }
  | { type: "setPrompt"; value: string }
  | { type: "setResults"; results: MatchResponse }
  | { type: "reset"; initialState: TripState };

function reducer(state: TripState, action: TripAction): TripState {
  switch (action.type) {
    case "addPeople": {
      const existingIds = new Set(state.people.map((p) => p.id));
      const newcomers = action.people.filter((p) => !existingIds.has(p.id));
      const newIds = action.people.map((p) => p.id);
      return {
        ...state,
        people: [...state.people, ...newcomers],
        selectedPersonIds: Array.from(
          new Set([...state.selectedPersonIds, ...newIds]),
        ),
      };
    }
    case "togglePerson": {
      const isSelected = state.selectedPersonIds.includes(action.id);
      return {
        ...state,
        selectedPersonIds: isSelected
          ? state.selectedPersonIds.filter((id) => id !== action.id)
          : [...state.selectedPersonIds, action.id],
      };
    }
    case "removePerson":
      return {
        ...state,
        people: state.people.filter((p) => p.id !== action.id),
        selectedPersonIds: state.selectedPersonIds.filter(
          (id) => id !== action.id,
        ),
      };
    case "setPrompt":
      return { ...state, prompt: action.value };
    case "setResults":
      return { ...state, lastResults: action.results };
    case "reset":
      return action.initialState;
    default:
      return state;
  }
}

interface TripContextValue extends TripState {
  addPeople: (people: Person[]) => void;
  togglePerson: (id: string) => void;
  removePerson: (id: string) => void;
  setPrompt: (value: string) => void;
  setResults: (results: MatchResponse) => void;
  reset: () => void;
}

const TripContext = createContext<TripContextValue | null>(null);

export function TripProvider({ children }: { children: ReactNode }) {
  const { user } = useSession();
  const initialState = useMemo<TripState>(
    () => ({
      people: [user],
      selectedPersonIds: [user.id],
      prompt: "",
      lastResults: null,
    }),
    [user],
  );
  const [state, dispatch] = useReducer(reducer, initialState);

  const value = useMemo<TripContextValue>(
    () => ({
      ...state,
      addPeople: (people) => dispatch({ type: "addPeople", people }),
      togglePerson: (id) => dispatch({ type: "togglePerson", id }),
      removePerson: (id) => dispatch({ type: "removePerson", id }),
      setPrompt: (value) => dispatch({ type: "setPrompt", value }),
      setResults: (results) => dispatch({ type: "setResults", results }),
      reset: () => dispatch({ type: "reset", initialState }),
    }),
    [state, initialState],
  );

  return <TripContext.Provider value={value}>{children}</TripContext.Provider>;
}

export function useTrip(): TripContextValue {
  const ctx = useContext(TripContext);
  if (!ctx) {
    throw new Error("useTrip must be used within a TripProvider");
  }
  return ctx;
}
