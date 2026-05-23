import { useEffect, useState } from "react";
import { Navigate, useNavigate, useParams } from "react-router-dom";
import { TotalPill } from "../components/TotalPill";
import { TripItemRow } from "../components/TripItemRow";
import { usePlannedTrips } from "../context/PlannedTripsContext";
import { useTrip } from "../context/TripContext";
import { bookTrip } from "../services/bookings";
import { getDestinationPackageBySlug } from "../services/destinations";
import type { DestinationPackage } from "../types/trip";

export function TripDetailsScreen() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const trip = useTrip();
  const { addPlannedTrip, plannedTrips } = usePlannedTrips();
  const [pkg, setPkg] = useState<DestinationPackage | null | undefined>(
    undefined,
  );

  useEffect(() => {
    if (!slug) return;
    getDestinationPackageBySlug(slug).then((p) => setPkg(p ?? null));
  }, [slug]);

  const plannedTrip = plannedTrips.find((t) => t.id === slug);
  const travelers = plannedTrip ? plannedTrip.people : trip.people;

  if (pkg === undefined) {
    return <div className="p-6 text-sm text-slate-500">Loading…</div>;
  }

  if (pkg === null || !slug) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="mx-auto flex w-full max-w-md flex-col gap-4 p-6">
      <button
        type="button"
        onClick={() => navigate("/")}
        className="self-start text-sm text-brand-blue hover:underline"
      >
        ← Back
      </button>

      <header className="text-center">
        <h1 className="text-3xl font-bold text-slate-800">
          {pkg.destinationName}
        </h1>
        {pkg.description && (
          <p className="text-sm text-slate-500">{pkg.description}</p>
        )}
        {travelers.length > 0 && (
          <div className="mt-3 flex flex-col items-center gap-2">
            <span className="text-base font-bold uppercase tracking-wider text-brand-blue">
              Travelers
            </span>
            <div className="flex flex-wrap justify-center gap-2">
              {travelers.map((p, idx) => (
                <span
                  key={`${p.name}-${idx}`}
                  className="rounded-full bg-brand-blue-soft px-4 py-1.5 text-base font-semibold text-brand-blue shadow-sm"
                >
                  {p.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </header>

      <TotalPill total={pkg.totalPrice} />

      {pkg.destinationsList.map((destination, dIdx) => (
        <section key={`${destination.name}-${dIdx}`} className="flex flex-col gap-4">
          {destination.cities.map((city) => (
            <div key={`${city.country}-${city.name}`} className="flex flex-col gap-2">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
                {city.name}, {city.country}
              </h2>
              <div className="divide-y divide-slate-100 rounded-2xl border border-slate-200 bg-white px-4 shadow-sm">
                <TripItemRow
                  name={city.accommodation.name}
                  price={city.accommodation.price}
                  category={{ kind: "accommodation" }}
                />
                {city.activityDetails.map((activity, aIdx) => (
                  <TripItemRow
                    key={`${activity.name}-${aIdx}`}
                    name={activity.name}
                    price={activity.price}
                    category={{ kind: "activity" }}
                  />
                ))}
              </div>
            </div>
          ))}

          {destination.transportation.length > 0 && (
            <div className="flex flex-col gap-2">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
                Transportation
              </h2>
              <div className="divide-y divide-slate-100 rounded-2xl border border-slate-200 bg-white px-4 shadow-sm">
                {destination.transportation.map((leg, lIdx) => (
                  <TripItemRow
                    key={`${leg.departure}-${leg.arrival}-${lIdx}`}
                    name={`${leg.departure} → ${leg.arrival} (${leg.transportationType})`}
                    price={leg.price}
                    category={{ kind: "transportation", type: leg.transportationType }}
                  />
                ))}
              </div>
            </div>
          )}
        </section>
      ))}

      {plannedTrip ? (
        <button
          type="button"
          onClick={async () => {
            await bookTrip({
              id: plannedTrip.id,
              destinationPackage: plannedTrip.destinationPackage,
              people: plannedTrip.people,
              prompt: plannedTrip.prompt,
              savedAt: plannedTrip.savedAt,
              bookedAt: Date.now(),
            });
            alert("Trip booked!");
          }}
          className="self-center rounded-full bg-brand-blue px-6 py-2 text-sm font-semibold text-white shadow-sm transition cursor-pointer hover:bg-brand-blue/90"
        >
          Book trip
        </button>
      ) : (
        <button
          type="button"
          onClick={() => {
            addPlannedTrip({
              id: slug,
              destinationPackage: pkg,
              people: trip.people,
              prompt: trip.prompt,
              savedAt: Date.now(),
            });
            trip.reset();
            navigate("/");
          }}
          className="self-center rounded-full bg-brand-blue px-6 py-2 text-sm font-semibold text-white shadow-sm transition cursor-pointer hover:bg-brand-blue/90"
        >
          Plan trip
        </button>
      )}
    </div>
  );
}
