from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TransportationType(str, Enum):
    flight = "Flight"
    bus = "Bus"
    train = "Train"


class TransportationMethod(str, Enum):
    flight = "Flight"
    car = "Car"
    train = "Train"


class Transportation(BaseModel):
    departure: str = Field(..., description="Departure location (airport, station, or city)", examples=["New York JFK"])
    arrival: str = Field(..., description="Arrival location (airport, station, or city)", examples=["Paris CDG"])
    transportationType: TransportationType = Field(..., description="Mode of transport: Flight, Bus, or Train")
    price: str = Field(..., description="Cost of the transportation leg", examples=["$650"])


class AccommodationDetails(BaseModel):
    name: str = Field(..., description="Name of the hotel or accommodation", examples=["Hotel Le Marais"])
    price: str = Field(..., description="Nightly rate", examples=["$150/night"])


class TransportationDetails(BaseModel):
    method: TransportationMethod


class ActivityDetails(BaseModel):
    name: str = Field(..., description="Name of the activity or attraction", examples=["Louvre Museum"])
    price: str = Field(..., description="Admission or participation cost", examples=["$20"])


class City(BaseModel):
    name: str = Field(..., description="City name", examples=["Paris"])
    country: str = Field(..., description="Country the city is in", examples=["France"])
    accommodation: AccommodationDetails = Field(..., description="Recommended accommodation in this city")
    activityDetails: list[ActivityDetails] = Field(..., description="List of recommended activities in this city")


class Destination(BaseModel):
    name: str = Field(..., description="Destination region or country name", examples=["Paris"])
    cities: list[City] = Field(..., description="Cities to visit within this destination")
    transportation: list[Transportation] = Field(..., description="Transportation legs to/within this destination")


class DestinationPackage(BaseModel):
    destinationsList: list[Destination] = Field(..., description="All destinations included in this package")
    destinationName: str = Field(..., description="Marketing name for the package", examples=["Paris & Rome Explorer"])
    totalPrice: str = Field(..., description="Estimated all-in cost for the trip", examples=["$3200"])
    description: Optional[str] = Field(None, description="Short human-readable summary of the package")
    picture: str = Field(..., description="URL of a representative cover photo", examples=["https://images.unsplash.com/photo-1499856871958-5b9627545d1a"])


class PromptResponseModel(BaseModel):
    departureDate: str = Field(..., description="ISO-8601 departure date extracted from the user's message", examples=["2025-07-01"])
    returnDate: str = Field(..., description="ISO-8601 return date extracted from the user's message", examples=["2025-07-10"])
    destinations: list[str] = Field(..., description="List of destination cities/countries mentioned", examples=[["Paris", "Rome"]])
    activities: list[str] = Field(..., description="Interests or activity types mentioned by the user", examples=[["food", "museums"]])


class PromptRequestModel(BaseModel):
    message: str = Field(..., description="Free-text natural-language travel request from the user", examples=["I want to visit Paris and Rome for 10 days in July, I love food and museums"])


class Summary(BaseModel):
    summary: list[DestinationPackage] = Field(..., description="List of curated destination packages matching the trip intent")

