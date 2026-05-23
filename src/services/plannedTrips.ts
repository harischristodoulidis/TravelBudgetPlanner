import type { PlannedTrip } from "../types/trip";

const KEY = "tbp.plannedTrips.v2";

export function loadPlannedTrips(): PlannedTrip[] {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as PlannedTrip[]) : [];
  } catch {
    return [];
  }
}

export function savePlannedTrips(trips: PlannedTrip[]): void {
  localStorage.setItem(KEY, JSON.stringify(trips));
}
