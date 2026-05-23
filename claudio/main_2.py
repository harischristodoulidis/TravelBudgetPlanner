import subprocess
import json
from destination_criteria import generate_travel_parameters, calculate_city_match

def execute_pipeline():
    """Executes all the data generation and profiling scripts in order."""
    print("\n🚀 [1/6] Generating Accommodations...")
    subprocess.run(["python3", "generate_accomodation.py"], check=True)
    
    print("🚀 [2/6] Generating Transportations...")
    subprocess.run(["python3", "generate_transport.py"], check=True)
    
    print("🚀 [3/6] Generating Activities...")
    subprocess.run(["python3", "generate_activities.py"], check=True)
    
    print("🚀 [4/6] Profiling User from CSV...")
    subprocess.run([
        "python3", "user_profiler_scikitlearn.py", 
        "user-1_hackathon10.csv", 
        "--user-id", "user_001", 
        "--output", "user_profile.json"
    ], check=True)
    
    print("🚀 [5/6] Profiling Cities...")
    subprocess.run(["python3", "city_profiler_teleport.py"], check=True)
    
    print("🚀 [6/6] Calculating Destination Leaderboard...\n")
    subprocess.run(["python3", "destination_criteria.py"], check=True)


def build_smart_itinerary():
    """Builds a personalized transportation itinerary."""
    print("\n=======================================================")
    print("🗺️   BUILDING SMART TRANSPORT ITINERARY              🗺️")
    print("=======================================================\n")
    
    origin = "Athens"
    with open("user_profile.json", "r") as f:
        user_data = json.load(f)
        
    profile = user_data.get("user_travel_profile", {})
    flat_profile = {}
    for section in ["spending_power", "experience_preferences", "movement_and_geography", "lifestyle_signals"]:
        if section in profile: flat_profile.update(profile[section])

    travel_params = generate_travel_parameters(flat_profile)
    user_budget = flat_profile.get("budget_capacity", 5.0)
    
    with open("city_profiles.json", "r") as f:
        cities_data = json.load(f)

    match_results = []
    for city_name, city_profile in cities_data.items():
        score = calculate_city_match(travel_params["destination_affinity_index"], city_profile)
        match_results.append({"city": city_name, "match": score["match_percentage"]})
        
    match_results = sorted(match_results, key=lambda x: x["match"], reverse=True)
    valid_destinations = [m for m in match_results if m["city"] != origin]
    
    top_1_city = valid_destinations[0]["city"]
    top_2_city = valid_destinations[1]["city"]
    
    print(f"📍 Origin: {origin}")
    print(f"🥇 Destination 1: {top_1_city} ({valid_destinations[0]['match']}% match)")
    print(f"🥈 Destination 2: {top_2_city} ({valid_destinations[1]['match']}% match)")
    print(f"💰 User Budget Score: {user_budget}/10\n")

    with open("transportations.json", "r") as f:
        transports = json.load(f)

    def select_best_transport(orig, dest, min_date=None):
        options = [t for t in transports if t["origin"] == orig and t["destination"] == dest]
        if min_date: options = [opt for opt in options if opt["departure_date"] > min_date]
        if not options: return None, None
            
        earliest_date = min(opt["departure_date"] for opt in options)
        daily_options = [opt for opt in options if opt["departure_date"] == earliest_date]
        daily_options = sorted(daily_options, key=lambda x: x["price"])
        
        if len(daily_options) == 1: return daily_options[0], "Only one transport option was available."
        if user_budget > 6.5: return daily_options[-1], f"Budget is {user_budget} (> 6.5), selected Premium option."
        else: return daily_options[0], f"Budget is {user_budget} (<= 6.5), selected Cheapest option."

    print(f"✈️  LEG 1: {origin} ➡️  {top_1_city}")
    leg1, r1 = select_best_transport(origin, top_1_city)
    if leg1:
        print(f"   ✅ [{leg1['departure_date']}] {leg1['company']} ({leg1['type']}) - {leg1['price']} {leg1['currency']}\n      💡 Why? {r1}")

    print(f"\n🚆 LEG 2: {top_1_city} ➡️  {top_2_city}")
    leg2_min_date = leg1['arrival_date'] if leg1 else None
    leg2, r2 = select_best_transport(top_1_city, top_2_city, leg2_min_date)
    if leg2:
        print(f"   ✅ [{leg2['departure_date']}] {leg2['company']} ({leg2['type']}) - {leg2['price']} {leg2['currency']}\n      💡 Why? {r2}")

    print(f"\n✈️  LEG 3 (RETURN): {top_2_city} ➡️  {origin}")
    leg3_min_date = leg2['arrival_date'] if leg2 else (leg2_min_date or "2026-08-01")
    leg3, r3 = select_best_transport(top_2_city, origin, leg3_min_date)
    if leg3:
        print(f"   ✅ [{leg3['departure_date']}] {leg3['company']} ({leg3['type']}) - {leg3['price']} {leg3['currency']}\n      💡 Why? {r3}")

    return {"top_1_city": top_1_city, "top_2_city": top_2_city, "leg1": leg1, "leg2": leg2, "leg3": leg3}


def build_smart_accommodation(itinerary):
    """Selects the best accommodation for each city based on strict Budget rules and Pace."""
    print("\n=======================================================")
    print("🏨   BUILDING SMART ACCOMMODATION PORTFOLIO          🏨")
    print("=======================================================\n")

    with open("user_profile.json", "r") as f: user_data = json.load(f)
    profile = user_data.get("user_travel_profile", {})
    budget = profile.get("spending_power", {}).get("budget_capacity", 5.0)
    pace = profile.get("experience_preferences", {}).get("pace_and_goal", 5.0)
    
    with open("accomodations.json", "r") as f: all_accs = json.load(f)

    def select_best_acc(city, check_in, check_out):
        city_accs = [a for a in all_accs if a["city"] == city]
        if not city_accs: return None, "No accommodations found."
        city_accs = sorted(city_accs, key=lambda x: x["price"])
        
        if budget < 2.5:
            allowed_accs = [a for a in city_accs if a["type"] != "hotel"] or city_accs
            if pace >= 6:
                hostels = [a for a in allowed_accs if a["type"] == "hostel"]
                selected, reason = (hostels[0] if hostels else allowed_accs[0]), "Budget < 2.5 and Pace is fast. Picked Hostel."
            else:
                bbs = [a for a in allowed_accs if a["type"] == "B&B"]
                selected, reason = (bbs[0] if bbs else allowed_accs[0]), "Budget < 2.5 but Pace is relaxed. Picked B&B."
        elif budget > 6.5:
            allowed_accs = [a for a in city_accs if a["type"] != "hostel"] or city_accs
            hotels = [a for a in allowed_accs if a["type"] == "hotel"]
            selected, reason = (hotels[-1] if hotels else allowed_accs[-1]), "Budget > 6.5. Picked premium Hotel."
        else:
            if pace >= 6:
                hostels = [a for a in city_accs if a["type"] == "hostel"]
                selected, reason = (hostels[0] if hostels else city_accs[0]), "Standard budget, fast pace. Picked Hostel."
            else:
                bbs = [a for a in city_accs if a["type"] in ["B&B", "hotel"]]
                selected, reason = (bbs[0] if bbs else city_accs[0]), "Standard budget, relaxed pace. Picked B&B/Hotel."

        selected["arrival_date"] = check_in
        selected["departure_date"] = check_out
        return selected, reason

    if itinerary["leg1"] and itinerary["leg2"]:
        city1, in1, out1 = itinerary["top_1_city"], itinerary["leg1"]["arrival_date"], itinerary["leg2"]["departure_date"]
        acc1, r1 = select_best_acc(city1, in1, out1)
        print(f"🛏️  STAY 1: {city1} ({in1} to {out1})\n   ✅ {acc1['name']} ({acc1['type'].upper()}) - {acc1['price']} {acc1['currency']}\n      💡 Why? {r1}\n")

    if itinerary["leg2"] and itinerary["leg3"]:
        city2, in2, out2 = itinerary["top_2_city"], itinerary["leg2"]["arrival_date"], itinerary["leg3"]["departure_date"]
        acc2, r2 = select_best_acc(city2, in2, out2)
        print(f"🛏️  STAY 2: {city2} ({in2} to {out2})\n   ✅ {acc2['name']} ({acc2['type'].upper()}) - {acc2['price']} {acc2['currency']}\n      💡 Why? {r2}\n")


def build_smart_activity(itinerary):
    """Selects ONE perfect activity per destination based on the user's personality traits."""
    print("=======================================================")
    print("🎟️   BUILDING SMART ACTIVITY ITINERARY               🎟️")
    print("=======================================================\n")

    # Load User Profile Scores
    with open("user_profile.json", "r") as f: user_data = json.load(f)
    profile = user_data.get("user_travel_profile", {})
    
    budget = profile.get("spending_power", {}).get("budget_capacity", 5.0)
    dining = profile.get("experience_preferences", {}).get("dining_sophistication", 5.0)
    culture = profile.get("experience_preferences", {}).get("cultural_engagement", 5.0)
    nightlife = profile.get("experience_preferences", {}).get("nightlife_propensity", 5.0)
    pace = profile.get("experience_preferences", {}).get("pace_and_goal", 5.0)
    nature = profile.get("lifestyle_signals", {}).get("nature_and_values", 5.0)

    print("📊 User Personality Traits:")
    print(f"   Budget: {budget} | Dining: {dining} | Culture: {culture}")
    print(f"   Nightlife: {nightlife} | Pace: {pace} | Nature: {nature}\n")

    # Load Activities
    with open("activities.json", "r") as f: all_activities = json.load(f)

    def select_best_activity(city, stay_date):
        city_acts = [a for a in all_activities if a["city"] == city]
        if not city_acts: return None, "No activities found."

        best_act = None
        highest_score = -999
        reasoning = ""

        for act in city_acts:
            score = 0
            act_type = act["type"]

            # 1. Base Score mapped directly to the user's traits
            if act_type == "cultural": score += culture
            elif act_type == "food": score += dining
            elif act_type == "nightlife": score += nightlife
            elif act_type == "natural": score += nature
            elif act_type == "relaxed": score += (11 - pace) # Low pace = high score for relaxed activities!

            # 2. Budget Guardrails
            if budget <= 4 and act["price"] > 100:
                score -= 20 # Heavily penalize expensive activities for budget travelers
            elif budget > 7 and act["price"] > 100:
                score += 3 # Boost premium activities for luxury travelers

            # 3. Check if it's the winner
            if score > highest_score:
                highest_score = score
                best_act = act
                
                # Format a nice string explaining the logic
                if act_type == "relaxed":
                    reasoning = f"User has a pace score of {pace} (prefers relaxed/spas). Activity score: {score}."
                elif budget <= 4 and act["price"] > 100:
                    reasoning = f"WARNING: Out of budget! But still chosen. Score: {score}."
                else:
                    reasoning = f"User has high interest in '{act_type}' (Score: {score}). Fits budget!"

        # Match the date to the user's actual time in the city
        best_act["arrival_date"] = stay_date
        best_act["departure_date"] = stay_date
        
        return best_act, reasoning

    # --- ACTIVITY 1 ---
    if itinerary["leg1"]:
        city1 = itinerary["top_1_city"]
        date1 = itinerary["leg1"]["arrival_date"] # Do the activity on the day they arrive
        
        act1, r1 = select_best_activity(city1, date1)
        print(f"🎯 ACTIVITY 1: {city1} ({date1})")
        print(f"   ✅ {act1['name']} ({act1['type'].upper()}) - {act1['price']} {act1['currency']}")
        print(f"      💡 Why? {r1}\n")

    # --- ACTIVITY 2 ---
    if itinerary["leg2"]:
        city2 = itinerary["top_2_city"]
        date2 = itinerary["leg2"]["arrival_date"]
        
        act2, r2 = select_best_activity(city2, date2)
        print(f"🎯 ACTIVITY 2: {city2} ({date2})")
        print(f"   ✅ {act2['name']} ({act2['type'].upper()}) - {act2['price']} {act2['currency']}")
        print(f"      💡 Why? {r2}\n")


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    execute_pipeline()
    itinerary = build_smart_itinerary()
    
    if itinerary:
        build_smart_accommodation(itinerary)
        build_smart_activity(itinerary)