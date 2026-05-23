import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AddPeopleButton } from "../components/AddPeopleButton";
import { ContactsModal } from "../components/ContactsModal";
import { DestinationCard } from "../components/DestinationCard";
import { PersonPill } from "../components/PersonPill";
import { PlannedTripCard } from "../components/PlannedTripCard";
import { PromptInput } from "../components/PromptInput";
import { usePlannedTrips } from "../context/PlannedTripsContext";
import { useSession } from "../context/SessionContext";
import { useTrip } from "../context/TripContext";
import { getMatches } from "../services/destinations";
import { slugify } from "../utils/slug";

export function PlanScreen() {
  const navigate = useNavigate();
  const trip = useTrip();
  const { user } = useSession();
  const { plannedTrips, removePlannedTrip } = usePlannedTrips();
  const [modalOpen, setModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [visibleCount, setVisibleCount] = useState(3);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const results = await getMatches(trip.prompt, trip.selectedPersonIds);
      trip.setResults(results);
      setVisibleCount(3);
    } finally {
      setSubmitting(false);
    }
  }

  const destinationPackages = trip.lastResults?.destinationPackages ?? [];
  const visible = destinationPackages.slice(0, visibleCount);
  const hasMore = destinationPackages.length > visibleCount;

  return (
    <div className="mx-auto flex w-full max-w-md flex-col gap-5 p-6">
      {plannedTrips.length > 0 && (
        <section>
          <h2 className="mb-2 text-sm font-semibold text-slate-600">
            Planned trips
          </h2>
          <div className="flex flex-col gap-2">
            {plannedTrips.map((t) => (
              <PlannedTripCard
                key={t.id}
                trip={t}
                onClick={() => navigate(`/trip/${t.id}`)}
                onRemove={() => removePlannedTrip(t.id)}
              />
            ))}
          </div>
        </section>
      )}

      <div>
        <AddPeopleButton onClick={() => setModalOpen(true)} />
      </div>

      <PromptInput
        value={trip.prompt}
        onChange={trip.setPrompt}
        onSubmit={handleSubmit}
        disabled={submitting}
      />

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

          <div className="flex flex-col gap-3">
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

          {hasMore && (
            <button
              type="button"
              onClick={() => setVisibleCount((c) => c + 3)}
              className="self-center rounded-full border border-brand-blue px-5 py-2 text-sm font-semibold text-brand-blue transition cursor-pointer hover:bg-brand-blue hover:text-white"
            >
              Add more
            </button>
          )}
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
    </div>
  );
}
