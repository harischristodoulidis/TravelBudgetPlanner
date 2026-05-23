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
      className="group flex w-full flex-col gap-2 text-left transition cursor-pointer"
    >
      <div className="relative aspect-square w-full overflow-hidden rounded-xl">
        <PackagePicture
          src={destination.picture}
          alt={destination.destinationName}
          className="h-full w-full object-cover transition group-hover:scale-105"
        />
      </div>
      <div className="flex min-w-0 flex-col">
        <span className="block w-full truncate text-sm font-semibold text-slate-800">
          {destination.destinationName}
        </span>
        <span className="text-xs text-slate-500">
          € {destination.totalPrice} · per person
        </span>
      </div>
    </button>
  );
}
