import json
import random

transportations = []

# ==========================================
# 1. OUTBOUND: Athens to Rome (Flights)
# ==========================================
outbound_dates = ["2026-08-01", "2026-08-02", "2026-08-05", "2026-08-08"]

for date_str in outbound_dates:
    # Standard cheap Ryanair flight
    transportations.append({
        "type": "airplane",
        "company": "Ryanair",
        "origin": "Athens",
        "destination": "Rome",
        "departure_date": date_str,
        "arrival_date": date_str,
        "price": random.randint(25, 85),
        "currency": "EUR"
    })
    
    # ONLY on Aug 1 and Aug 2, add an expensive Aegean flight
    if date_str in ["2026-08-01", "2026-08-02"]:
        transportations.append({
            "type": "airplane",
            "company": "Aegean",
            "origin": "Athens",
            "destination": "Rome",
            "departure_date": date_str,
            "arrival_date": date_str,
            "price": random.randint(180, 280),
            "currency": "EUR"
        })

# ==========================================
# 2. MID-TRIP: Rome to Florence (Train & Bus)
# ==========================================
mid_trip_dates = ["2026-08-05", "2026-08-06"]

for date_str in mid_trip_dates:
    # Trenitalia Train
    transportations.append({
        "type": "train",
        "company": "Trenitalia",
        "origin": "Rome",
        "destination": "Florence",
        "departure_date": date_str,
        "arrival_date": date_str,
        "price": random.randint(35, 55),
        "currency": "EUR"
    })
    
    # Flixbus Bus
    transportations.append({
        "type": "bus",
        "company": "Flixbus",
        "origin": "Rome",
        "destination": "Florence",
        "departure_date": date_str,
        "arrival_date": date_str,
        "price": random.randint(15, 25),
        "currency": "EUR"
    })

# ==========================================
# 3. RETURN: Florence to Athens (Flights)
# ==========================================
return_dates_florence = ["2026-08-22", "2026-08-23"]

for date_str in return_dates_florence:
    # Aegean is the only airline for this route
    transportations.append({
        "type": "airplane",
        "company": "Aegean",
        "origin": "Florence",
        "destination": "Athens",
        "departure_date": date_str,
        "arrival_date": date_str,
        "price": random.randint(110, 190), # Usually a bit more expensive from Florence
        "currency": "EUR"
    })

# Save the generated list to a JSON file
filename = "mock/transportations.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(transportations, json_file, indent=4)

print(f"All data has been perfectly formatted and saved to: {filename}")