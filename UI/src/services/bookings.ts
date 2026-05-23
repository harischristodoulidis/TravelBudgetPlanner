import { postDestPackage } from "./api";
import type { BookTripRequest } from "../types/trip";

export async function bookTrip(payload: BookTripRequest): Promise<void> {
  await postDestPackage(payload.destinationPackage);
}
