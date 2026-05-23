import type { BookTripRequest } from "../types/trip";

// TODO: replace with real fetch once backend endpoint is live
export function bookTrip(payload: BookTripRequest): Promise<void> {
  console.log("[bookTrip] payload to POST:", payload);
  return Promise.resolve();
}
