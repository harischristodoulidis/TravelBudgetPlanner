from pydantic import BaseModel
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
    departure: str
    arrival: str
    transportationType: TransportationType
    price: str


class AccommodationDetails(BaseModel):
    name: str
    price: str


class TransportationDetails(BaseModel):
    method: TransportationMethod


class ActivityDetails(BaseModel):
    name: str
    price: str


class City(BaseModel):
    name: str
    country: str
    accommodation: AccommodationDetails
    activityDetails: list[ActivityDetails]


class Destination(BaseModel):
    name: str
    cities: list[City]
    transportation: list[Transportation]


class DestinationPackage(BaseModel):
    destinationsList: list[Destination]
    destinationName: str
    totalPrice: str
    description: Optional[str] = None
    picture: str


class PromptResponseModel(BaseModel):
    departureDate: str
    returnDate: str
    destinations: list[str]
    activities: list[str]


class PromptRequestModel(BaseModel):
    message: str

class Summary(BaseModel): 
    summary: list[DestinationPackage]

