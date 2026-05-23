from .models import (
    DestinationPackage,
    Destination,
    City,
    Transportation,
    AccommodationDetails,
    TransportationDetails,
    ActivityDetails,
    TransportationType,
    TransportationMethod,
)

MOCK_PACKAGES: list[DestinationPackage] = [
    DestinationPackage(
        destinationName="European Highlights",
        totalPrice="2850",
        description="A scenic journey through Paris and Rome covering art, cuisine, and culture.",
        picture="https://images.unsplash.com/photo-1499856843078-a8c50d4e3d32",
        destinationsList=[
            Destination(
                name="France",
                transportation=[
                    Transportation(
                        departure="Athens",
                        arrival="Paris",
                        transportationType=TransportationType.flight,
                        price="180",
                    )
                ],
                cities=[
                    City(
                        name="Paris",
                        country="France",
                        accommodation=AccommodationDetails(
                            name="Hotel Le Marais",
                            price="120",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.car,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Eiffel Tower", price="25"),
                            ActivityDetails(name="Louvre Museum", price="17"),
                            ActivityDetails(name="Seine River Cruise", price="15"),
                        ],
                    )
                ],
            ),
            Destination(
                name="Italy",
                transportation=[
                    Transportation(
                        departure="Paris",
                        arrival="Rome",
                        transportationType=TransportationType.train,
                        price="95",
                    )
                ],
                cities=[
                    City(
                        name="Rome",
                        country="Italy",
                        accommodation=AccommodationDetails(
                            name="Colosseo Boutique Hotel",
                            price="110",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.train,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Colosseum Tour", price="18"),
                            ActivityDetails(name="Vatican Museums", price="20"),
                            ActivityDetails(name="Trevi Fountain Area Walk", price="0"),
                        ],
                    )
                ],
            ),
        ],
    ),
    DestinationPackage(
        destinationName="Iberian Adventure",
        totalPrice="1950",
        description="Explore the vibrant cities of Barcelona and Lisbon.",
        picture="https://images.unsplash.com/photo-1539037116277-4db20889f2d4",
        destinationsList=[
            Destination(
                name="Spain",
                transportation=[
                    Transportation(
                        departure="Athens",
                        arrival="Barcelona",
                        transportationType=TransportationType.flight,
                        price="160",
                    )
                ],
                cities=[
                    City(
                        name="Barcelona",
                        country="Spain",
                        accommodation=AccommodationDetails(
                            name="Gothic Quarter Inn",
                            price="95",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.car,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Sagrada Familia", price="26"),
                            ActivityDetails(name="Park Güell", price="10"),
                            ActivityDetails(name="Camp Nou Stadium Tour", price="28"),
                        ],
                    )
                ],
            ),
            Destination(
                name="Portugal",
                transportation=[
                    Transportation(
                        departure="Barcelona",
                        arrival="Lisbon",
                        transportationType=TransportationType.flight,
                        price="75",
                    )
                ],
                cities=[
                    City(
                        name="Lisbon",
                        country="Portugal",
                        accommodation=AccommodationDetails(
                            name="Alfama View Hostel",
                            price="60",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.train,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Belém Tower", price="6"),
                            ActivityDetails(name="Jerónimos Monastery", price="10"),
                            ActivityDetails(name="Fado Night Show", price="35"),
                        ],
                    )
                ],
            ),
        ],
    ),
    DestinationPackage(
        destinationName="Aegean Escape",
        totalPrice="1200",
        description="A relaxing island-hopping trip across the Greek Aegean.",
        picture="https://images.unsplash.com/photo-1533105079780-92b9be482077",
        destinationsList=[
            Destination(
                name="Greece",
                transportation=[
                    Transportation(
                        departure="Athens",
                        arrival="Santorini",
                        transportationType=TransportationType.flight,
                        price="80",
                    ),
                    Transportation(
                        departure="Santorini",
                        arrival="Mykonos",
                        transportationType=TransportationType.bus,
                        price="40",
                    ),
                ],
                cities=[
                    City(
                        name="Santorini",
                        country="Greece",
                        accommodation=AccommodationDetails(
                            name="Caldera Cliffside Suites",
                            price="150",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.car,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Oia Sunset Walk", price="0"),
                            ActivityDetails(name="Akrotiri Archaeological Site", price="12"),
                            ActivityDetails(name="Catamaran Cruise", price="85"),
                        ],
                    ),
                    City(
                        name="Mykonos",
                        country="Greece",
                        accommodation=AccommodationDetails(
                            name="Little Venice Studios",
                            price="130",
                        ),
                        trans=TransportationDetails(
                            method=TransportationMethod.car,
                        ),
                        activityDetails=[
                            ActivityDetails(name="Windmills of Kato Mili", price="0"),
                            ActivityDetails(name="Delos Island Day Trip", price="20"),
                            ActivityDetails(name="Paradise Beach Club", price="15"),
                        ],
                    ),
                ],
            )
        ],
    ),
]


def get_mock_packages() -> list[DestinationPackage]:
    return MOCK_PACKAGES
