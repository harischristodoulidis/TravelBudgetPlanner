import { Bus, Hotel, Plane, Ticket, TrainFront, type LucideIcon } from "lucide-react";
import { TransportationType } from "../types/trip";

export type TripItemCategory =
  | { kind: "accommodation" }
  | { kind: "activity" }
  | { kind: "transportation"; type: TransportationType };

interface TripItemRowProps {
  name: string;
  price: string;
  category: TripItemCategory;
}

function iconFor(category: TripItemCategory): LucideIcon {
  switch (category.kind) {
    case "accommodation":
      return Hotel;
    case "activity":
      return Ticket;
    case "transportation":
      switch (category.type) {
        case TransportationType.Flight:
          return Plane;
        case TransportationType.Bus:
          return Bus;
        case TransportationType.Train:
          return TrainFront;
      }
  }
}

export function TripItemRow({ name, price, category }: TripItemRowProps) {
  const Icon = iconFor(category);
  return (
    <div className="flex items-center gap-3 py-3">
      <Icon aria-hidden className="h-5 w-5 shrink-0 text-brand-blue" />
      <div className="flex flex-1 flex-col">
        <span className="text-sm font-semibold text-slate-800">{name}</span>
      </div>
      <span className="text-sm font-medium text-slate-800">€ {price}</span>
    </div>
  );
}
