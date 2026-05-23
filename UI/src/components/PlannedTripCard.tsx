import type { DestinationPackage } from "../types/trip";
import { PackagePicture } from "./PackagePicture";

interface PlannedTripCardProps {
  pkg: DestinationPackage;
  onClick: () => void;
  onRemove: () => void;
}

export function PlannedTripCard({
  pkg,
  onClick,
  onRemove,
}: PlannedTripCardProps) {
  return (
    <div className="relative">
      <button
        type="button"
        onClick={onClick}
        className="flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-white p-2.5 pr-10 text-left shadow-sm transition hover:border-brand-blue hover:shadow-md"
      >
        <PackagePicture
          src={pkg.picture}
          alt={pkg.destinationName}
          className="h-10 w-10 flex-shrink-0 rounded-lg object-cover"
        />
        <div className="flex flex-1 flex-col">
          <span className="text-sm font-semibold text-slate-800">
            {pkg.destinationName}
          </span>
          {pkg.description && (
            <span className="text-xs text-slate-500">{pkg.description}</span>
          )}
        </div>
        <span className="text-sm font-semibold text-slate-800">
          € {pkg.totalPrice}
        </span>
      </button>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          onRemove();
        }}
        aria-label={`Remove ${pkg.destinationName}`}
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
