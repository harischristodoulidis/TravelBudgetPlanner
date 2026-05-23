import { useState } from "react";
import { Navigate, useNavigate, useParams } from "react-router-dom";
import { TotalPill } from "../components/TotalPill";
import { TripItemRow } from "../components/TripItemRow";
import { usePlannedTrips } from "../context/PlannedTripsContext";
import { useTrip } from "../context/TripContext";
import { bookTrip } from "../services/bookings";
import { slugify } from "../utils/slug";

export function TripDetailsScreen() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const trip = useTrip();
  const { addPlannedTrip, plannedTrips, removePlannedTrip } = usePlannedTrips();
  const [booking, setBooking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const plannedTrip = plannedTrips.find((t) => t.id === slug);
  const suggested = trip.lastResults?.destinationPackages.find(
    (p) => slugify(p.destinationName) === slug,
  );
  const pkg = plannedTrip?.destinationPackage ?? suggested ?? null;
  const travelers = plannedTrip ? plannedTrip.people : trip.people;

  if (!slug || !pkg) {
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
        <>
          <button
            type="button"
            disabled={booking}
            onClick={async () => {
              setBooking(true);
              setError(null);
              try {
                await Promise.all([
                  bookTrip({
                    id: plannedTrip.id,
                    destinationPackage: plannedTrip.destinationPackage,
                    people: plannedTrip.people,
                    prompt: plannedTrip.prompt,
                    savedAt: plannedTrip.savedAt,
                    bookedAt: Date.now(),
                  }),
                  new Promise((resolve) => setTimeout(resolve, 1000)),
                ]);
                removePlannedTrip(plannedTrip.id);
                navigate("/");
              } catch {
                setError("Could not book trip. Please try again.");
                setBooking(false);
              }
            }}
            className="self-center flex items-center justify-center min-w-[110px] rounded-full bg-brand-blue px-6 py-2 text-sm font-semibold text-white shadow-sm transition cursor-pointer hover:bg-brand-blue/90 disabled:cursor-not-allowed disabled:opacity-80"
          >
            {booking ? (
              <svg
                className="h-4 w-4 animate-spin"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden
              >
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeOpacity="0.25"
                  strokeWidth="4"
                />
                <path
                  d="M22 12a10 10 0 0 1-10 10"
                  stroke="currentColor"
                  strokeWidth="4"
                  strokeLinecap="round"
                />
              </svg>
            ) : (
              "Book trip"
            )}
          </button>
          {error && (
            <p className="self-center text-sm text-red-500">{error}</p>
          )}
        </>
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
