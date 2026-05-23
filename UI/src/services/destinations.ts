import type {
  Destination,
  DestinationPackage,
  MatchResponse,
} from "../types/trip";
import { TransportationType } from "../types/trip";
import { slugify } from "../utils/slug";

const theatreDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Rome",
      country: "Italy",
      accommodation: { name: "Hotel 1", price: "50" },
      activityDetails: [],
    },
    {
      name: "Florence",
      country: "Italy",
      accommodation: { name: "Hotel 2", price: "50" },
      activityDetails: [{ name: "Live Show", price: "150" }],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Rome",
      transportationType: TransportationType.Flight,
      price: "50",
    },
    {
      departure: "Rome airport",
      arrival: "Rome city center",
      transportationType: TransportationType.Train,
      price: "8",
    },
    {
      departure: "Rome",
      arrival: "Florence",
      transportationType: TransportationType.Train,
      price: "20",
    },
    {
      departure: "Florence city center",
      arrival: "Florence airport",
      transportationType: TransportationType.Train,
      price: "8",
    },
    {
      departure: "Florence",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "19",
    },
  ],
};

const cultureDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Rome",
      country: "Italy",
      accommodation: { name: "Boutique Hotel Centro", price: "110" },
      activityDetails: [
        { name: "Colosseum + Forum tour", price: "75" },
        { name: "Vatican Museums", price: "55" },
      ],
    },
    {
      name: "Florence",
      country: "Italy",
      accommodation: { name: "Hotel Duomo View", price: "120" },
      activityDetails: [
        { name: "Uffizi Gallery", price: "60" },
        { name: "Accademia (David)", price: "35" },
      ],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Rome",
      transportationType: TransportationType.Flight,
      price: "60",
    },
    {
      departure: "Rome airport",
      arrival: "Rome city center",
      transportationType: TransportationType.Train,
      price: "8",
    },
    {
      departure: "Rome",
      arrival: "Florence",
      transportationType: TransportationType.Train,
      price: "45",
    },
    {
      departure: "Florence city center",
      arrival: "Florence airport",
      transportationType: TransportationType.Train,
      price: "8",
    },
    {
      departure: "Florence",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "224",
    },
  ],
};

const summerDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Rome",
      country: "Italy",
      accommodation: { name: "Trastevere Loft", price: "70" },
      activityDetails: [{ name: "Rooftop aperitivo crawl", price: "40" }],
    },
    {
      name: "Florence",
      country: "Italy",
      accommodation: { name: "Oltrarno B&B", price: "80" },
      activityDetails: [
        { name: "Chianti vineyard day trip", price: "130" },
        { name: "Sunset on Piazzale Michelangelo", price: "0" },
      ],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Rome",
      transportationType: TransportationType.Flight,
      price: "45",
    },
    {
      departure: "Rome airport",
      arrival: "Rome city center",
      transportationType: TransportationType.Train,
      price: "14",
    },
    {
      departure: "Rome",
      arrival: "Florence",
      transportationType: TransportationType.Train,
      price: "25",
    },
    {
      departure: "Florence city center",
      arrival: "Florence airport",
      transportationType: TransportationType.Bus,
      price: "7",
    },
    {
      departure: "Florence",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "159",
    },
  ],
};

function totalOf(destinations: Destination[]): string {
  let sum = 0;
  for (const destination of destinations) {
    for (const city of destination.cities) {
      sum += Number(city.accommodation.price);
      for (const activity of city.activityDetails) {
        sum += Number(activity.price);
      }
    }
    for (const leg of destination.transportation) {
      sum += Number(leg.price);
    }
  }
  return String(sum);
}

function buildPackage(
  destinationName: string,
  description: string,
  pictureSeed: string,
  destination: Destination,
): DestinationPackage {
  const destinationsList = [destination];
  return {
    destinationName,
    description,
    picture: `https://picsum.photos/seed/${pictureSeed}/160/160`,
    destinationsList,
    totalPrice: totalOf(destinationsList),
  };
}

const foodieDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Bologna",
      country: "Italy",
      accommodation: { name: "Casa Pasta", price: "90" },
      activityDetails: [
        { name: "Pasta-making class", price: "65" },
        { name: "Mercato di Mezzo food tour", price: "45" },
      ],
    },
    {
      name: "Modena",
      country: "Italy",
      accommodation: { name: "Balsamico B&B", price: "85" },
      activityDetails: [{ name: "Balsamic vinegar tasting", price: "30" }],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Bologna",
      transportationType: TransportationType.Flight,
      price: "95",
    },
    {
      departure: "Bologna",
      arrival: "Modena",
      transportationType: TransportationType.Train,
      price: "10",
    },
    {
      departure: "Modena",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "110",
    },
  ],
};

const adventureDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Dolomites",
      country: "Italy",
      accommodation: { name: "Alpine Lodge", price: "140" },
      activityDetails: [
        { name: "Guided hike to Tre Cime", price: "80" },
        { name: "Via ferrata day", price: "120" },
      ],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Venice",
      transportationType: TransportationType.Flight,
      price: "70",
    },
    {
      departure: "Venice",
      arrival: "Dolomites",
      transportationType: TransportationType.Bus,
      price: "25",
    },
    {
      departure: "Dolomites",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "85",
    },
  ],
};

const coastalDestination: Destination = {
  name: "Italy",
  cities: [
    {
      name: "Amalfi",
      country: "Italy",
      accommodation: { name: "Cliffside Suites", price: "180" },
      activityDetails: [
        { name: "Capri boat tour", price: "95" },
        { name: "Path of the Gods hike", price: "0" },
      ],
    },
    {
      name: "Positano",
      country: "Italy",
      accommodation: { name: "Villa Limone", price: "200" },
      activityDetails: [{ name: "Sunset sailing", price: "75" }],
    },
  ],
  transportation: [
    {
      departure: "Athens",
      arrival: "Naples",
      transportationType: TransportationType.Flight,
      price: "80",
    },
    {
      departure: "Naples",
      arrival: "Amalfi",
      transportationType: TransportationType.Bus,
      price: "15",
    },
    {
      departure: "Amalfi",
      arrival: "Positano",
      transportationType: TransportationType.Bus,
      price: "5",
    },
    {
      departure: "Positano",
      arrival: "Athens",
      transportationType: TransportationType.Flight,
      price: "120",
    },
  ],
};

const PACKAGES: DestinationPackage[] = [
  buildPackage(
    "Italy - Theatre",
    "Theather and night life",
    "italy-theatre",
    theatreDestination,
  ),
  buildPackage(
    "Italy - Culture",
    "Monuments and culture",
    "italy-culture",
    cultureDestination,
  ),
  buildPackage(
    "Italy - Summer",
    "Summer vibes",
    "italy-summer",
    summerDestination,
  ),
  buildPackage(
    "Italy - Foodie",
    "Pasta, balsamico and food tours",
    "italy-foodie",
    foodieDestination,
  ),
  buildPackage(
    "Italy - Adventure",
    "Hiking and via ferrata in the Dolomites",
    "italy-adventure",
    adventureDestination,
  ),
  buildPackage(
    "Italy - Coastal",
    "Amalfi coast escape",
    "italy-coastal",
    coastalDestination,
  ),
];

export function getMatches(
  prompt: string,
  _peopleIds: string[],
): Promise<MatchResponse> {
  const summary = prompt.trim()
    ? "Hello, here are some trips that might fit your group."
    : "Hello, here are some trips that might fit your group.";
  return Promise.resolve({
    summary,
    destinationPackages: PACKAGES,
  });
}

export function getDestinationPackageBySlug(
  slug: string,
): Promise<DestinationPackage | undefined> {
  return Promise.resolve(
    PACKAGES.find((pkg) => slugify(pkg.destinationName) === slug),
  );
}
