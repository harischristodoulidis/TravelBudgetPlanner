import json
import random
from datetime import date, timedelta

# Create an empty list to hold all our generated accommodation data
accommodations = []

# Set our date range
start_date = date(2026, 8, 1)
end_date = date(2026, 8, 20)

# Define our mock database of properties with their base price PER NIGHT
properties = {
    "Rome": [
        {"name": "Hotel Roma", "type": "hotel", "company": "Booking.com", "base_price": 100},
        {"name": "Hotel Luxor", "type": "hotel", "company": "Booking.com", "base_price": 160},
        {"name": "Ludovico Apartment", "type": "B&B", "company": "Airbnb", "base_price": 180}, # Expensive Airbnb
        {"name": "Mario and Luigi Brothers", "type": "B&B", "company": "Airbnb", "base_price": 80},  # Cheaper Airbnb
        {"name": "YellowSquare Hostel", "type": "hostel", "company": "Hostelworld", "base_price": 35}
    ],
    "Florence": [
        {"name": "Hotel Michelangelo", "type": "hotel", "company": "Booking.com", "base_price": 150},
        {"name": "Firenze Centro", "type": "hotel", "company": "Booking.com", "base_price": 110},
        {"name": "Uffizi Romantic Loft", "type": "B&B", "company": "Airbnb", "base_price": 210}, # Expensive Airbnb
        {"name": "Tuscan Dream B&B", "type": "B&B", "company": "Airbnb", "base_price": 95},
        {"name": "Plus Florence", "type": "hostel", "company": "Hostelworld", "base_price": 40}
    ],
    "Athens": [
        {"name": "Acropolis Palace", "type": "hotel", "company": "Booking.com", "base_price": 140},
        {"name": "Parthenon Inn", "type": "hotel", "company": "Booking.com", "base_price": 90},
        {"name": "Plaka Vibes Suite", "type": "B&B", "company": "Airbnb", "base_price": 175}, # Expensive Airbnb
        {"name": "Zeus Studio", "type": "B&B", "company": "Airbnb", "base_price": 75},
        {"name": "Athens Backpackers", "type": "hostel", "company": "Hostelworld", "base_price": 30}
    ]
}

current_date = start_date

# Loop through every single day from Aug 1 to Aug 20
while current_date <= end_date:
    
    # Generate both a 3-night stay and a 4-night stay starting on this date
    for nights in [3, 4]:
        departure_date = current_date + timedelta(days=nights)
        
        # Stop generating if the checkout date goes past August 20th
        if departure_date > end_date:
            continue
            
        arrival_str = current_date.strftime("%Y-%m-%d")
        departure_str = departure_date.strftime("%Y-%m-%d")
        
        # Loop through every city and every property
        for city, props in properties.items():
            for prop in props:
                
                # Add random price fluctuation per night (-10 to +30 euros)
                daily_rate = prop["base_price"] + random.randint(-10, 30)
                total_price = daily_rate * nights
                
                # Append to our main list in the exact format you requested
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

    # Move to the next day
    current_date += timedelta(days=1)

# Save the generated list to a JSON file
filename = "accomodations.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(accommodations, json_file, indent=4)

print(f"All data has been perfectly formatted and saved to: {filename}")