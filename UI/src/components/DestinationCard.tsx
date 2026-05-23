import type { DestinationPackage } from "../types/trip";
import { PackagePicture } from "./PackagePicture";

type DestinationCardProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  destination: DestinationPackage;
};

export function DestinationCard({
  destination,
  ...props
}: DestinationCardProps) {
  return (
    <button
      {...props}
      type="button"
      className="flex w-full items-center gap-4 rounded-2xl border border-slate-200 bg-white p-3 text-left shadow-sm transition hover:border-brand-blue hover:shadow-md"
    >
      <PackagePicture
        src={destination.picture}
        alt={destination.destinationName}
        className="h-20 w-20 flex-shrink-0 rounded-xl object-cover"
      />
      <div className="flex flex-1 flex-col">
        <span className="text-lg font-semibold text-slate-800">
          {destination.destinationName}
        </span>
        {destination.description && (
          <span className="text-xs text-slate-500">
            {destination.description}
          </span>
        )}
      </div>
      <div className="flex flex-col items-end">
        <span className="text-base font-semibold text-slate-800">
          € {destination.totalPrice}
        </span>
        <span className="text-[10px] uppercase tracking-wide text-slate-400">
          per person
        </span>
      </div>
    </button>
  );
}
