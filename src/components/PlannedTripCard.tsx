import type { PlannedTrip } from "../types/trip";

interface PlannedTripCardProps {
  trip: PlannedTrip;
  onClick: () => void;
  onRemove: () => void;
}

export function PlannedTripCard({
  trip,
  onClick,
  onRemove,
}: PlannedTripCardProps) {
  const { destinationPackage, people } = trip;
  const extra = people.length - 1;

  return (
    <div className="relative">
      <button
        type="button"
        onClick={onClick}
        className="flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-white p-2.5 pr-10 text-left shadow-sm transition hover:border-brand-blue hover:shadow-md"
      >
        <img
          src={destinationPackage.picture}
          alt={destinationPackage.destinationName}
          loading="lazy"
          className="h-10 w-10 flex-shrink-0 rounded-lg object-cover"
        />
        <div className="flex flex-1 flex-col">
          <span className="text-sm font-semibold text-slate-800">
            {destinationPackage.destinationName}
          </span>
          {destinationPackage.description && (
            <span className="text-xs text-slate-500">
              {destinationPackage.description}
            </span>
          )}
          {extra > 0 && (
            <span className="text-[11px] text-slate-400">
              with {extra} {extra === 1 ? "other" : "others"}
            </span>
          )}
        </div>
        <span className="text-sm font-semibold text-slate-800">
          € {destinationPackage.totalPrice}
        </span>
      </button>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          onRemove();
        }}
        aria-label={`Remove ${destinationPackage.destinationName}`}
        className="absolute right-2 top-2 flex h-6 w-6 items-center justify-center rounded-full bg-slate-100 text-slate-500 transition hover:bg-slate-200 hover:text-slate-700"
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
    </div>
  );
}
