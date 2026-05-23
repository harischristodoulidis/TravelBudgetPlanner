import json
import random
from datetime import date, timedelta

# Create an empty list to hold all our generated activities
activities_list = []

# Set our date range
start_date = date(2026, 8, 1)
end_date = date(2026, 8, 20)

# UPDATED Hackathon constraint: Added "food"
VALID_TYPES = ["relaxed", "natural", "cultural", "nightlife", "food"]

# Define our mock database of activities and restaurants
catalog = [
    # --- ROME ---
    {"city": "Rome", "type": "cultural", "company": "Vatican Museums", "name": "Vatican Museums tour", "price": 35, "days": [0,1,2,3,4,5]},
    {"city": "Rome", "type": "cultural", "company": "CoopCulture", "name": "Colosseum tour", "price": 25, "days": [1,2,3,4,5,6]},
    {"city": "Rome", "type": "natural", "company": "Green Tours", "name": "Appian Way E-Bike", "price": 45, "days": [2, 5]},
    {"city": "Rome", "type": "relaxed", "company": "QC Terme", "name": "Roman Thermal Baths", "price": 55, "days": [0,1,2,3,4,5,6]},
    {"city": "Rome", "type": "nightlife", "company": "Rome Pub Crawl", "name": "Trastevere Bar Tour", "price": 30, "days": [4, 5]},
    {"city": "Rome", "type": "nightlife", "company": "Ticketone", "name": "Metallica concert", "price": 120, "days": [], "specific_dates": ["2026-08-03"]},
    # Rome Food
    {"city": "Rome", "type": "food", "company": "La Pergola", "name": "3-Michelin Star Tasting Menu", "price": 290, "days": [1,2,3,4,5]}, # Closed Sun/Mon, Very Expensive
    {"city": "Rome", "type": "food", "company": "Il Margutta", "name": "Gourmet Vegan Dinner", "price": 45, "days": [0,1,2,3,4,5,6]}, # Vegan
    
    # --- FLORENCE ---
    {"city": "Florence", "type": "cultural", "company": "Uffizi Gallery", "name": "Uffizi Masterpieces", "price": 28, "days": [1,2,3,4,5,6]},
    {"city": "Florence", "type": "relaxed", "company": "Tuscany Tastes", "name": "Chianti Wine Tasting", "price": 65, "days": [3, 4, 5]},
    {"city": "Florence", "type": "natural", "company": "Green Tours", "name": "Boboli Gardens Sunset", "price": 15, "days": [0, 2, 6]},
    {"city": "Florence", "type": "nightlife", "company": "Firenze Events", "name": "Florence Jazz Festival", "price": 50, "days": [], "specific_dates": ["2026-08-10", "2026-08-11"]},
    # Florence Food
    {"city": "Florence", "type": "food", "company": "Enoteca Pinchiorri", "name": "Exclusive Wine & Dine", "price": 320, "days": [1,2,3,4,5]}, # Closed Sun/Mon, Very Expensive
    {"city": "Florence", "type": "food", "company": "Raw Vegan Firenze", "name": "Organic Vegan Lunch", "price": 25, "days": [0,1,2,3,4,5]}, # Closed Sundays, Vegan

    # --- ATHENS ---
    {"city": "Athens", "type": "cultural", "company": "Athens Walking Tours", "name": "Acropolis Guided Tour", "price": 40, "days": [0,1,2,3,4,5,6]},
    {"city": "Athens", "type": "natural", "company": "Hike Greece", "name": "Mount Lycabettus Hike", "price": 20, "days": [1, 3]},
    {"city": "Athens", "type": "relaxed", "company": "Cine Paris", "name": "Open Air Cinema Plaka", "price": 12, "days": [], "specific_dates": ["2026-08-05", "2026-08-12", "2026-08-19"]},
    {"city": "Athens", "type": "nightlife", "company": "Gazi Clubs", "name": "Bouzoukia Live Night", "price": 80, "days": [4, 5]},
    # Athens Food
    {"city": "Athens", "type": "food", "company": "Spondi", "name": "Acropolis View Fine Dining", "price": 180, "days": [0,1,2,3,4,5,6]}, # Very Expensive
    {"city": "Athens", "type": "food", "company": "Vegan Beat", "name": "Vegan Greek Street Food", "price": 18, "days": [0,1,2,3,4,5,6]} # Vegan
]

# Safety Check: Guarantee that no typos slipped into our catalog
for item in catalog:
    assert item["type"] in VALID_TYPES, f"ERROR: '{item['type']}' is not a valid type!"

current_date = start_date

# Loop through every single day
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    weekday = current_date.weekday()
    
    for item in catalog:
        runs_today = False
        
        if "specific_dates" in item and date_str in item["specific_dates"]:
            runs_today = True
        elif "days" in item and weekday in item["days"]:
            runs_today = True
            
        # 20% chance it is sold out / fully booked to simulate empty days
        if runs_today and (random.random() < 0.8):
            activities_list.append({
                "type": item["type"],
                "company": item["company"],
                "city": item["city"],
                "name": item["name"],
                "arrival_date": date_str,      
                "departure_date": date_str,    
                "price": item["price"],
                "currency": "EUR"
            })

    current_date += timedelta(days=1)

# Save the generated list to a JSON file
filename = "activities.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(activities_list, json_file, indent=4)

print(f"All data has been perfectly formatted and saved to: {filename}")