import json
import random

# Create an empty list to hold our exact 12 activities
activities_list = []

# Define the EXACT dates for each city's activities
city_dates = {
    "Rome": "2026-08-03",
    "Florence": "2026-08-07",
    "Athens": "2026-08-25"
}

# Define our mock database grouped by city
# We removed the "days" and "specific_dates" logic because we are forcing the dates now.
catalog = {
    "Rome": [
        {"type": "cultural", "company": "Vatican Museums", "name": "Vatican Museums tour", "price": 35},
        {"type": "cultural", "company": "CoopCulture", "name": "Colosseum tour", "price": 25},
        {"type": "natural", "company": "Green Tours", "name": "Appian Way E-Bike", "price": 45},
        {"type": "relaxed", "company": "QC Terme", "name": "Roman Thermal Baths", "price": 55},
        {"type": "nightlife", "company": "Rome Pub Crawl", "name": "Trastevere Bar Tour", "price": 30},
        {"type": "nightlife", "company": "Ticketone", "name": "Metallica concert", "price": 120},
        {"type": "food", "company": "La Pergola", "name": "3-Michelin Star Tasting Menu", "price": 290}, 
        {"type": "food", "company": "Il Margutta", "name": "Gourmet Vegan Dinner", "price": 45}
    ],
    "Florence": [
        {"type": "cultural", "company": "Uffizi Gallery", "name": "Uffizi Masterpieces", "price": 28},
        {"type": "relaxed", "company": "Tuscany Tastes", "name": "Chianti Wine Tasting", "price": 65},
        {"type": "natural", "company": "Green Tours", "name": "Boboli Gardens Sunset", "price": 15},
        {"type": "nightlife", "company": "Firenze Events", "name": "Florence Jazz Festival", "price": 50},
        {"type": "food", "company": "Enoteca Pinchiorri", "name": "Exclusive Wine & Dine", "price": 320},
        {"type": "food", "company": "Raw Vegan Firenze", "name": "Organic Vegan Lunch", "price": 25}
    ],
    "Athens": [
        {"type": "cultural", "company": "Athens Walking Tours", "name": "Acropolis Guided Tour", "price": 40},
        {"type": "natural", "company": "Hike Greece", "name": "Mount Lycabettus Hike", "price": 20},
        {"type": "relaxed", "company": "Cine Paris", "name": "Open Air Cinema Plaka", "price": 12},
        {"type": "nightlife", "company": "Gazi Clubs", "name": "Bouzoukia Live Night", "price": 80},
        {"type": "food", "company": "Spondi", "name": "Acropolis View Fine Dining", "price": 180},
        {"type": "food", "company": "Vegan Beat", "name": "Vegan Greek Street Food", "price": 18}
    ]
}

# Loop through our 3 cities and their assigned dates
for city, fixed_date in city_dates.items():
    
    # Randomly pick exactly 4 activities from that city's catalog
    selected_activities = random.sample(catalog[city], 4)
    
    for item in selected_activities:
        activities_list.append({
            "type": item["type"],
            "company": item["company"],
            "city": city,
            "name": item["name"],
            "arrival_date": fixed_date,      
            "departure_date": fixed_date,    
            "price": item["price"],
            "currency": "EUR"
        })

# Save the generated list to a JSON file
filename = "mock/activities.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(activities_list, json_file, indent=4)

print(f"Success! Exactly 12 activities (4 per city) have been perfectly formatted and saved to: {filename}")