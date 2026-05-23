import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AddPeopleButton } from "../components/AddPeopleButton";
import { ConfirmModal } from "../components/ConfirmModal";
import { ContactsModal } from "../components/ContactsModal";
import { DestinationCard } from "../components/DestinationCard";
import { PersonPill } from "../components/PersonPill";
import { PlannedTripCard } from "../components/PlannedTripCard";
import { PromptInput } from "../components/PromptInput";
import { useSession } from "../context/SessionContext";
import { useTrip } from "../context/TripContext";
import {
  deleteDestPackage,
  fetchDestPackages,
  postPrompt,
  postSuggestions,
} from "../services/api";
import type { DestinationPackage } from "../types/trip";
import { slugify } from "../utils/slug";

export function PlanScreen() {
  const navigate = useNavigate();
  const trip = useTrip();
  const { user } = useSession();
  const [modalOpen, setModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [plannedPackages, setPlannedPackages] = useState<DestinationPackage[]>(
    [],
  );
  const [pendingRemoval, setPendingRemoval] =
    useState<DestinationPackage | null>(null);

  useEffect(() => {
    fetchDestPackages()
      .then(setPlannedPackages)
      .catch(() => {});
  }, []);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const intent = await postPrompt(trip.prompt);
      trip.setPromptIntent(intent);
      const packages = await postSuggestions(intent);
      trip.setResults({
        summary: "Hello, here are some trips that might fit your group.",
        destinationPackages: packages,
      });
    } finally {
      setSubmitting(false);
    }
  }

  const destinationPackages = trip.lastResults?.destinationPackages ?? [];
  const visible = destinationPackages.slice(0, 10);

  return (
    <div className="mx-auto flex w-full max-w-md flex-col gap-5 p-6 md:max-w-6xl">
      {plannedPackages.length > 0 && (
        <section>
          <h2 className="mb-2 text-sm font-semibold text-slate-600">
            Planned trips
          </h2>
          <div className="grid grid-cols-4 gap-2">
            {plannedPackages.map((pkg, i) => (
              <PlannedTripCard
                key={`${pkg.destinationName}-${i}`}
                pkg={pkg}
                onClick={() =>
                  navigate(`/trip/${slugify(pkg.destinationName)}`)
                }
                onRemove={() => setPendingRemoval(pkg)}
              />
            ))}
          </div>
        </section>
      )}

      <div className="flex flex-col gap-2">
        <div>
          <h2 className="text-xl font-semibold text-slate-800">
            Plan your next trip
          </h2>
          <p className="text-base text-slate-500">
            Tell us where you'd like to go, who's coming, and your budget — we'll
            suggest destinations that fit.
          </p>
        </div>
        <PromptInput
          value={trip.prompt}
          onChange={trip.setPrompt}
          onSubmit={handleSubmit}
          disabled={submitting}
          leftSlot={<AddPeopleButton onClick={() => setModalOpen(true)} />}
        />
      </div>

      <div className="flex flex-wrap gap-2">
        {trip.people.map((person) => {
          const isSelf = person.id === user.id;
          return (
            <PersonPill
              key={person.id}
              name={person.name}
              isSelf={isSelf}
              onRemove={isSelf ? undefined : () => trip.removePerson(person.id)}
            />
          );
        })}
      </div>

      {trip.lastResults && (
        <>
          <p className="text-sm text-slate-600">{trip.lastResults.summary}</p>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
            {visible.map((d) => {
              const slug = slugify(d.destinationName);
              return (
                <DestinationCard
                  key={slug}
                  destination={d}
                  onClick={() => navigate(`/trip/${slug}`)}
                />
              );
            })}
          </div>
        </>
      )}

      {modalOpen && (
        <ContactsModal
          alreadySelectedIds={trip.people.map((p) => p.id)}
          onClose={() => setModalOpen(false)}
          onConfirm={(people) => {
            trip.addPeople(people);
            setModalOpen(false);
          }}
        />
      )}

      {pendingRemoval && (
        <ConfirmModal
          title="Remove planned trip"
          message={`Remove "${pendingRemoval.destinationName}" from your planned trips?`}
          onCancel={() => setPendingRemoval(null)}
          onConfirm={async () => {
            const target = pendingRemoval;
            setPendingRemoval(null);
            try {
              await deleteDestPackage(target.destinationName);
              setPlannedPackages((prev) =>
                prev.filter(
                  (p) => p.destinationName !== target.destinationName,
                ),
              );
            } catch {
              fetchDestPackages()
                .then(setPlannedPackages)
                .catch(() => {});
            }
          }}
        />
      )}
    </div>
  );
}
