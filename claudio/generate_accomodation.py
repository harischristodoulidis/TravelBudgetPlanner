import json
import random

# Create an empty list to hold our EXACTLY 9 properties
accommodations = []

# Define our mock database with FIXED base prices PER NIGHT
properties = {
    "Rome": [
        {"name": "Hotel Roma", "type": "hotel", "company": "Booking.com", "base_price": 70},
        {"name": "Hotel Luxor", "type": "hotel", "company": "Booking.com", "base_price": 160},
        {"name": "Ludovico Apartment", "type": "B&B", "company": "Airbnb", "base_price": 180},
        {"name": "Mario and Luigi Brothers", "type": "B&B", "company": "Airbnb", "base_price": 80},
        {"name": "YellowSquare Hostel", "type": "hostel", "company": "Hostelworld", "base_price": 35}
    ],
    "Florence": [
        {"name": "Hotel Michelangelo", "type": "hotel", "company": "Booking.com", "base_price": 150},
        {"name": "Firenze Centro", "type": "hotel", "company": "Booking.com", "base_price": 110},
        {"name": "Uffizi Romantic Loft", "type": "B&B", "company": "Airbnb", "base_price": 210},
        {"name": "Tuscan Dream B&B", "type": "B&B", "company": "Airbnb", "base_price": 65},
        {"name": "Plus Florence", "type": "hostel", "company": "Hostelworld", "base_price": 40}
    ],
    "Athens": [
        {"name": "Acropolis Palace", "type": "hotel", "company": "Booking.com", "base_price": 140},
        {"name": "Parthenon Inn", "type": "hotel", "company": "Booking.com", "base_price": 90},
        {"name": "Plaka Vibes Suite", "type": "B&B", "company": "Airbnb", "base_price": 175},
        {"name": "Zeus Studio", "type": "B&B", "company": "Airbnb", "base_price": 75},
        {"name": "Athens Backpackers", "type": "hostel", "company": "Hostelworld", "base_price": 30}
    ]
}

# Fix the dates for our simple 9-item demo
arrival_str = "2026-08-01"
departure_str = "2026-08-05"
nights = 3

# Loop through the 3 cities
for city, props in properties.items():
    
    # Randomly pick EXACTLY 3 properties from the 5 available options
    selected_properties = random.sample(props, 3)
    
    for prop in selected_properties:
        
        # FIXED PRICE: Base price exactly multiplied by the number of nights
        total_price = prop["base_price"] * nights
        
        # Append to our list
        accommodations.append({
            "type": prop["type"],
            "company": prop["company"],
            "city": city,
            "name": prop["name"],
            "destination": city,
            "arrival_date": arrival_str,
            "departure_date": departure_str,
            "price": total_price,
            "currency": "EUR"
        })

# Save the generated list to a JSON file
filename = "accomodations.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(accommodations, json_file, indent=4)

print(f"Success! Exactly 9 accommodations (with fixed prices) have been saved to: {filename}")