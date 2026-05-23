import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useReducer,
  type ReactNode,
} from "react";
import { loadPlannedTrips, savePlannedTrips } from "../services/plannedTrips";
import type { PlannedTrip } from "../types/trip";

type Action =
  | { type: "add"; trip: PlannedTrip }
  | { type: "remove"; id: string };

function reducer(state: PlannedTrip[], action: Action): PlannedTrip[] {
  switch (action.type) {
    case "add": {
      const without = state.filter((t) => t.id !== action.trip.id);
      return [action.trip, ...without];
    }
    case "remove":
      return state.filter((t) => t.id !== action.id);
    default:
      return state;
  }
}

interface PlannedTripsContextValue {
  plannedTrips: PlannedTrip[];
  addPlannedTrip: (trip: PlannedTrip) => void;
  removePlannedTrip: (id: string) => void;
}

const PlannedTripsContext = createContext<PlannedTripsContextValue | null>(
  null,
);

export function PlannedTripsProvider({ children }: { children: ReactNode }) {
  const [plannedTrips, dispatch] = useReducer(
    reducer,
    undefined,
    loadPlannedTrips,
  );

  useEffect(() => {
    savePlannedTrips(plannedTrips);
  }, [plannedTrips]);

  const value = useMemo<PlannedTripsContextValue>(
    () => ({
      plannedTrips,
      addPlannedTrip: (trip) => dispatch({ type: "add", trip }),
      removePlannedTrip: (id) => dispatch({ type: "remove", id }),
    }),
    [plannedTrips],
  );

  return (
    <PlannedTripsContext.Provider value={value}>
      {children}
    </PlannedTripsContext.Provider>
  );
}

export function usePlannedTrips(): PlannedTripsContextValue {
  const ctx = useContext(PlannedTripsContext);
  if (!ctx) {
    throw new Error(
      "usePlannedTrips must be used within a PlannedTripsProvider",
    );
  }
  return ctx;
}
