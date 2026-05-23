import json
import random
from datetime import date, timedelta

# Create an empty list to hold all our generated travel routes
transportations = []

# Set our date range (August 1 to August 20, 2026)
start_date = date(2026, 8, 1)
end_date = date(2026, 8, 20)

# Helper function to generate realistic price fluctuations
def get_price(base, min_var, max_var):
    return base + random.randint(min_var, max_var)

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Get the day of the week (0 = Monday, 1 = Tuesday ... 6 = Sunday)
    weekday = current_date.weekday() 
    
    # ==========================================
    # 1. Athens to Rome (Flights)
    # ==========================================
    # Ryanair: 3 times a week (Mon, Wed, Fri)
    if weekday in [0, 2, 4]:
        transportations.append({
            "type": "airplane",
            "company": "Ryanair",
            "origin": "Athens",
            "destination": "Rome",
            "departure_date": date_str,
            "arrival_date": date_str,
            "price": get_price(45, -5, 20), # Price between 40 - 65
            "currency": "EUR"
        })
        
    # Aegean: 2 times a week (Tue, Sat)
    if weekday in [1, 5]:
        transportations.append({
            "type": "airplane",
            "company": "Aegean",
            "origin": "Athens",
            "destination": "Rome",
            "departure_date": date_str,
            "arrival_date": date_str,
            "price": get_price(85, -10, 25), # Price between 75 - 110
            "currency": "EUR"
        })

    # ==========================================
    # 2. Rome to Florence (Train & Bus)
    # ==========================================
    # Trenitalia: Every single day
    transportations.append({
        "type": "train",
        "company": "Trenitalia",
        "origin": "Rome",
        "destination": "Florence",
        "departure_date": date_str,
        "arrival_date": date_str,
        "price": get_price(42, -5, 12), # Price between 37 - 54
        "currency": "EUR"
    })
    
    # Flixbus: 2 times a week (Thu, Sun)
    if weekday in [3, 6]:
        transportations.append({
            "type": "bus",
            "company": "Flixbus",
            "origin": "Rome",
            "destination": "Florence",
            "departure_date": date_str,
            "arrival_date": date_str,
            "price": get_price(18, -3, 7), # Price between 15 - 25
            "currency": "EUR"
        })

    # ==========================================
    # 3. Florence to Athens (Flights)
    # ==========================================
    # Aegean: 2 times a week (Wed, Sun)
    if weekday in [2, 6]:
        transportations.append({
            "type": "airplane",
            "company": "Aegean",
            "origin": "Florence",
            "destination": "Athens",
            "departure_date": date_str,
            "arrival_date": date_str,
            "price": get_price(120, -15, 30), # Price between 105 - 150
            "currency": "EUR"
        })

    # Move to the next day in the loop
    current_date += timedelta(days=1)

# Save the generated list to a JSON file
filename = "transportations.json"
with open(filename, 'w', encoding='utf-8') as json_file:
    json.dump(transportations, json_file, indent=4)

print(f"All data has been perfectly formatted and saved to: {filename}")