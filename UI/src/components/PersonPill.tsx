interface PersonPillProps {
  name: string;
  isSelf?: boolean;
  onRemove?: () => void;
}

export function PersonPill({ name, isSelf, onRemove }: PersonPillProps) {
  return (
    <div
      className={`inline-flex items-center gap-2 rounded-full bg-brand-blue py-1.5 pl-4 text-sm font-semibold text-white shadow-sm ${
        onRemove ? "pr-1.5" : "pr-4"
      }`}
    >
      <span>
        {name}
        {isSelf && (
          <span className="ml-1 font-normal text-white/70">(me)</span>
        )}
      </span>
      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          aria-label={`Remove ${name}`}
          className="flex h-5 w-5 items-center justify-center rounded-full bg-brand-blue-soft text-brand-blue transition hover:bg-white"
        >
          <svg viewBox="0 0 12 12" className="h-3 w-3" aria-hidden>
            <path
              d="M3 3 L9 9 M9 3 L3 9"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            />
          </svg>
        </button>
      )}
    </div>
  );
}
