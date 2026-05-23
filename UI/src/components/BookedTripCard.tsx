import type { DestinationPackage } from "../types/trip";
import { PackagePicture } from "./PackagePicture";

interface BookedTripCardProps {
  pkg: DestinationPackage;
}

export function BookedTripCard({ pkg }: BookedTripCardProps) {
  return (
    <div className="flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-white p-2.5 shadow-sm">
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
    </div>
  );
}
