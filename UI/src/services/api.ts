import type { DestinationPackage } from "../types/trip";

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface BackendUser {
  userId: string;
  username: string;
  passwordHash: string;
  firstName: string;
  lastName: string;
  friendIds: string[];
  createdAt: string;
}

export interface PromptResponse {
  departureDate: string;
  returnDate: string;
  destinations: string[];
  activities: string[];
}

interface SuggestionsResponse {
  summary: DestinationPackage[];
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`${init?.method ?? "GET"} ${path} failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export function fetchUsers(): Promise<BackendUser[]> {
  return request<BackendUser[]>("/users");
}

export function postPrompt(message: string): Promise<PromptResponse> {
  return request<PromptResponse>("/prompt", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

export async function postSuggestions(
  intent: PromptResponse,
): Promise<DestinationPackage[]> {
  const res = await request<SuggestionsResponse>("/suggestions", {
    method: "POST",
    body: JSON.stringify(intent),
  });
  return res.summary;
}

export function postDestPackage(
  pkg: DestinationPackage,
): Promise<{ status: string }> {
  return request<{ status: string }>("/destPackage", {
    method: "POST",
    body: JSON.stringify(pkg),
  });
}

export function fetchDestPackages(): Promise<DestinationPackage[]> {
  return request<DestinationPackage[]>("/destPackage");
}
