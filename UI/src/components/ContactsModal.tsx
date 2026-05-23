import { useEffect, useState } from "react";
import { fetchUsers, type BackendUser } from "../services/api";
import type { Person } from "../types/trip";

interface ContactsModalProps {
  alreadySelectedIds: string[];
  onClose: () => void;
  onConfirm: (people: Person[]) => void;
}

function toPerson(user: BackendUser): Person {
  return {
    id: user.userId,
    name: `${user.firstName} ${user.lastName}`.trim() || user.username,
  };
}

export function ContactsModal({
  alreadySelectedIds,
  onClose,
  onConfirm,
}: ContactsModalProps) {
  const [contacts, setContacts] = useState<Person[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [picked, setPicked] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState("");

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchUsers()
      .then((users) => {
        if (cancelled) return;
        setContacts(users.map(toPerson));
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Failed to load users");
      })
      .finally(() => {
        if (cancelled) return;
        setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const query = search.trim().toLowerCase();
  const availableContacts = contacts.filter(
    (c) =>
      !alreadySelectedIds.includes(c.id) &&
      (query === "" || c.name.toLowerCase().includes(query)),
  );

  function toggle(id: string) {
    setPicked((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  function confirm() {
    const chosen = contacts.filter((c) => picked.has(c.id));
    onConfirm(chosen);
  }

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-sm rounded-2xl bg-white p-5 shadow-xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-3 flex items-center justify-between border-b border-slate-200 pb-3">
          <h2 className="text-base font-semibold text-slate-800">
            Add travel companions
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="flex h-7 w-7 items-center justify-center rounded-full text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
          >
            <svg viewBox="0 0 14 14" className="h-3.5 w-3.5" aria-hidden>
              <path
                d="M3 3 L11 11 M11 3 L3 11"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search companions"
          className="mb-3 w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700 placeholder:text-slate-400 focus:border-brand-blue focus:outline-none"
        />
        {loading ? (
          <p className="mb-4 text-sm text-slate-400">Loading companions…</p>
        ) : error ? (
          <p className="mb-4 text-sm text-red-500">
            Could not load companions. {error}
          </p>
        ) : availableContacts.length === 0 ? (
          <p className="mb-4 text-sm text-slate-400">
            {query
              ? "No contacts match your search."
              : "All your contacts are already added."}
          </p>
        ) : (
          <ul className="mb-4 max-h-72 space-y-1 overflow-auto">
            {availableContacts.map((c) => {
              const isPicked = picked.has(c.id);
              return (
                <li key={c.id}>
                  <button
                    type="button"
                    onClick={() => toggle(c.id)}
                    className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm transition hover:bg-brand-blue-soft"
                  >
                    <span>{c.name}</span>
                    <span
                      aria-hidden
                      className={`h-4 w-4 rounded-full border ${
                        isPicked
                          ? "border-brand-blue bg-brand-blue"
                          : "border-slate-300"
                      }`}
                    />
                  </button>
                </li>
              );
            })}
          </ul>
        )}
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-3 py-2 text-sm text-slate-600 cursor-pointer hover:bg-slate-100"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={confirm}
            disabled={picked.size === 0}
            className="rounded-lg bg-brand-blue px-4 py-2 text-sm font-medium text-white shadow-sm transition cursor-pointer hover:opacity-90 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            Add {picked.size > 0 ? `(${picked.size})` : ""}
          </button>
        </div>
      </div>
    </div>
  );
}
