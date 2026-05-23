export interface Person {
  id: string;
  name: string;
}

export enum TransportationType {
  Flight = "Flight",
  Bus = "Bus",
  Train = "Train",
}

export enum TransportationMethod {
  Flight = "Flight",
  Car = "Car",
  Train = "Train",
}

export interface Transportation {
  departure: string;
  arrival: string;
  transportationType: TransportationType;
  price: string;
}

export interface AccommodationDetails {
  name: string;
  price: string;
}

export interface TransportationDetails {
  method: TransportationMethod;
}

export interface ActivityDetails {
  name: string;
  price: string;
}

export interface City {
  name: string;
  country: string;
  accommodation: AccommodationDetails;
  activityDetails: ActivityDetails[];
}

export interface Destination {
  name: string;
  cities: City[];
  transportation: Transportation[];
}

export interface DestinationPackage {
  destinationsList: Destination[];
  destinationName: string;
  totalPrice: string;
  description?: string;
  picture: string;
}

export interface MatchResponse {
  summary: string;
  destinationPackages: DestinationPackage[];
}

export interface PlannedTrip {
  id: string;
  destinationPackage: DestinationPackage;
  people: Person[];
  prompt: string;
  savedAt: number;
}

export interface BookTripRequest {
  id: string;
  destinationPackage: DestinationPackage;
  people: Person[];
  prompt: string;
  savedAt: number;
  bookedAt: number;
}
