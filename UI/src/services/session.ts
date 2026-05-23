import type { Person } from "../types/trip";

const KEY = "tbp.session.v1";

export interface Session {
  sessionId: string;
  user: Person;
}

export const MOCK_BANK_USERS: Person[] = [
  { id: "user-claudio", name: "Claudio" },
];

function isValidSession(value: unknown): value is Session {
  if (!value || typeof value !== "object") return false;
  const s = value as Partial<Session>;
  if (typeof s.sessionId !== "string") return false;
  if (!s.user || typeof s.user !== "object") return false;
  return typeof s.user.id === "string" && typeof s.user.name === "string";
}

export function loadSession(): Session | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return isValidSession(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

export function saveSession(session: Session): void {
  localStorage.setItem(KEY, JSON.stringify(session));
}

export function getOrCreateSession(): Session {
  const existing = loadSession();
  if (existing) return existing;

  const session: Session = {
    sessionId: crypto.randomUUID(),
    user: MOCK_BANK_USERS[0],
  };
  saveSession(session);
  return session;
}
