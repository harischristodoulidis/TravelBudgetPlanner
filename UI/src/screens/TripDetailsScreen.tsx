import { useEffect, useState } from "react";
import { Navigate, useNavigate, useParams } from "react-router-dom";
import { PackagePicture } from "../components/PackagePicture";
import { TotalPill } from "../components/TotalPill";
import { TripItemRow } from "../components/TripItemRow";
import { useTrip } from "../context/TripContext";
import { fetchDestPackages, postDestPackage } from "../services/api";
import type { DestinationPackage } from "../types/trip";
import { slugify } from "../utils/slug";

export function TripDetailsScreen() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const trip = useTrip();
  const [plannedPackages, setPlannedPackages] = useState<DestinationPackage[]>(
    [],
  );
  const [planning, setPlanning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDestPackages()
      .then(setPlannedPackages)
      .catch(() => {});
  }, []);

  const planned = plannedPackages.find(
    (p) => slugify(p.destinationName) === slug,
  );
  const suggested = trip.lastResults?.destinationPackages.find(
    (p) => slugify(p.destinationName) === slug,
  );
  const pkg = planned ?? suggested ?? null;
  const isPlanned = !!planned;
  const travelers = isPlanned ? [] : trip.people;

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

      <div className="relative aspect-video w-full overflow-hidden rounded-3xl shadow-sm">
        <PackagePicture
          src={pkg.picture}
          alt={pkg.destinationName}
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-linear-to-t from-black/70 via-black/20 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 p-5 text-white">
          <h1 className="text-3xl font-bold drop-shadow">
            {pkg.destinationName}
          </h1>
          {pkg.description && (
            <p className="mt-1 text-sm text-white/85 drop-shadow">
              {pkg.description}
            </p>
          )}
        </div>
      </div>

      {travelers.length > 0 && (
        <div className="flex flex-col items-center gap-2">
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

      {!isPlanned && (
        <>
          <button
            type="button"
            disabled={planning}
            onClick={async () => {
              setPlanning(true);
              setError(null);
              try {
                await Promise.all([
                  postDestPackage(pkg),
                  new Promise((resolve) => setTimeout(resolve, 1000)),
                ]);
                trip.reset();
                navigate("/");
              } catch {
                setError("Could not save trip. Please try again.");
                setPlanning(false);
              }
            }}
            className="self-center flex items-center justify-center min-w-27.5 rounded-full bg-brand-blue px-6 py-2 text-sm font-semibold text-white shadow-sm transition cursor-pointer hover:bg-brand-blue/90 disabled:cursor-not-allowed disabled:opacity-80"
          >
            {planning ? (
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
              "Plan trip"
            )}
          </button>
          {error && (
            <p className="self-center text-sm text-red-500">{error}</p>
          )}
        </>
      )}
    </div>
  );
}
