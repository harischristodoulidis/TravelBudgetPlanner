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
        "--output", "output/user_profile.json"
    ], check=True)

    print("🚀 [5/6] Profiling Cities...")
    subprocess.run(["python3", "city_profiler_teleport.py"], check=True)

    print("🚀 [6/6] Calculating Destination Leaderboard...\n")
    subprocess.run(["python3", "destination_criteria.py"], check=True)


def build_smart_itinerary():
    """Builds a personalized transportation itinerary. Returns a dict with legs and city selections."""
    origin = "Athens"
    with open("output/user_profile.json", "r") as f:
        user_data = json.load(f)

    profile = user_data.get("user_travel_profile", {})
    flat_profile = {}
    for section in ["spending_power", "experience_preferences", "movement_and_geography", "lifestyle_signals"]:
        if section in profile: flat_profile.update(profile[section])

    travel_params = generate_travel_parameters(flat_profile)
    user_budget = flat_profile.get("budget_capacity", 5.0)

    with open("mock/city_profiles.json", "r") as f:
        cities_data = json.load(f)

    match_results = []
    for city_name, city_profile in cities_data.items():
        score = calculate_city_match(travel_params["destination_affinity_index"], city_profile)
        match_results.append({"city": city_name, "match": score["match_percentage"]})

    match_results = sorted(match_results, key=lambda x: x["match"], reverse=True)
    valid_destinations = [m for m in match_results if m["city"] != origin]

    top_1_city = valid_destinations[0]["city"]
    top_2_city = valid_destinations[1]["city"]

    with open("mock/transportations.json", "r") as f:
        transports = json.load(f)

    def select_best_transport(orig, dest, min_date=None):
        options = [t for t in transports if t["origin"] == orig and t["destination"] == dest]
        if min_date: options = [opt for opt in options if opt["departure_date"] > min_date]
        if not options: return None
        earliest_date = min(opt["departure_date"] for opt in options)
        daily_options = sorted([opt for opt in options if opt["departure_date"] == earliest_date], key=lambda x: x["price"])
        if len(daily_options) == 1: return daily_options[0]
        return daily_options[-1] if user_budget > 6.5 else daily_options[0]

    leg1 = select_best_transport(origin, top_1_city)
    leg2 = select_best_transport(top_1_city, top_2_city, leg1["arrival_date"] if leg1 else None)
    leg3 = select_best_transport(top_2_city, origin, leg2["arrival_date"] if leg2 else "2026-08-01")

    return {
        "origin": origin,
        "top_1_city": top_1_city,
        "top_2_city": top_2_city,
        "user_budget": user_budget,
        "leg1": leg1,
        "leg2": leg2,
        "leg3": leg3,
    }


def build_smart_accommodation(itinerary):
    """Selects the best accommodation per city. Returns {city_name: accommodation_dict}."""
    with open("output/user_profile.json", "r") as f: user_data = json.load(f)
    profile = user_data.get("user_travel_profile", {})
    budget = profile.get("spending_power", {}).get("budget_capacity", 5.0)
    pace = profile.get("experience_preferences", {}).get("pace_and_goal", 5.0)

    with open("mock/accomodations.json", "r") as f: all_accs = json.load(f)

    def select_best_acc(city, check_in, check_out):
        city_accs = sorted([a for a in all_accs if a["city"] == city], key=lambda x: x["price"])
        if not city_accs: return None

        if budget < 2.5:
            allowed = [a for a in city_accs if a["type"] != "hotel"] or city_accs
            pool = [a for a in allowed if a["type"] == "hostel"] if pace >= 6 else [a for a in allowed if a["type"] == "B&B"]
            selected = (pool or allowed)[0]
        elif budget > 6.5:
            allowed = [a for a in city_accs if a["type"] != "hostel"] or city_accs
            hotels = [a for a in allowed if a["type"] == "hotel"]
            selected = (hotels or allowed)[-1]
        else:
            if pace >= 6:
                hostels = [a for a in city_accs if a["type"] == "hostel"]
                selected = (hostels or city_accs)[0]
            else:
                bbs = [a for a in city_accs if a["type"] in ["B&B", "hotel"]]
                selected = (bbs or city_accs)[0]

        selected["check_in"] = check_in
        selected["check_out"] = check_out
        return selected

    result = {}
    if itinerary["leg1"] and itinerary["leg2"]:
        city1 = itinerary["top_1_city"]
        result[city1] = select_best_acc(city1, itinerary["leg1"]["arrival_date"], itinerary["leg2"]["departure_date"])
    if itinerary["leg2"] and itinerary["leg3"]:
        city2 = itinerary["top_2_city"]
        result[city2] = select_best_acc(city2, itinerary["leg2"]["arrival_date"], itinerary["leg3"]["departure_date"])
    return result


def build_smart_activity(itinerary):
    """Selects ONE best activity per destination. Returns {city_name: activity_dict}."""
    with open("output/user_profile.json", "r") as f: user_data = json.load(f)
    profile = user_data.get("user_travel_profile", {})

    budget   = profile.get("spending_power", {}).get("budget_capacity", 5.0)
    dining   = profile.get("experience_preferences", {}).get("dining_sophistication", 5.0)
    culture  = profile.get("experience_preferences", {}).get("cultural_engagement", 5.0)
    nightlife= profile.get("experience_preferences", {}).get("nightlife_propensity", 5.0)
    pace     = profile.get("experience_preferences", {}).get("pace_and_goal", 5.0)
    nature   = profile.get("lifestyle_signals", {}).get("nature_and_values", 5.0)

    with open("mock/activities.json", "r") as f: all_activities = json.load(f)

    def select_best_activity(city, stay_date):
        city_acts = [a for a in all_activities if a["city"] == city]
        if not city_acts: return None
        best_act, highest_score = None, -999
        for act in city_acts:
            score = {"cultural": culture, "food": dining, "nightlife": nightlife,
                     "natural": nature, "relaxed": 11 - pace}.get(act["type"], 0)
            if budget <= 4 and act["price"] > 100: score -= 20
            elif budget > 7 and act["price"] > 100: score += 3
            if score > highest_score:
                highest_score, best_act = score, act
        best_act["date"] = stay_date
        return best_act

    result = {}
    if itinerary["leg1"]:
        city1 = itinerary["top_1_city"]
        result[city1] = select_best_activity(city1, itinerary["leg1"]["arrival_date"])
    if itinerary["leg2"]:
        city2 = itinerary["top_2_city"]
        result[city2] = select_best_activity(city2, itinerary["leg2"]["arrival_date"])
    return result


def build_package(itinerary, accommodations, activities):
    """Assembles all results into a packages.json-compatible dict."""
    city1, city2 = itinerary["top_1_city"], itinerary["top_2_city"]
    leg1, leg2, leg3 = itinerary["leg1"], itinerary["leg2"], itinerary["leg3"]

    TYPE_MAP = {"airplane": "Flight", "train": "Train", "bus": "Bus"}

    def to_transport(leg):
        if not leg: return None
        return {
            "departure": leg["origin"],
            "arrival": leg["destination"],
            "transportationType": TYPE_MAP.get(leg["type"].lower(), leg["type"].capitalize()),
            "price": str(leg["price"])
        }

    def to_acc(acc):
        if not acc: return {}
        return {"name": acc["name"], "price": str(acc["price"])}

    def to_activity(act):
        if not act: return []
        return [{"name": act["name"], "price": str(act["price"])}]

    acc1, acc2 = accommodations.get(city1), accommodations.get(city2)
    act1, act2 = activities.get(city1), activities.get(city2)

    total = sum([
        leg1["price"] if leg1 else 0,
        leg2["price"] if leg2 else 0,
        leg3["price"] if leg3 else 0,
        acc1["price"] if acc1 else 0,
        acc2["price"] if acc2 else 0,
        act1["price"] if act1 else 0,
        act2["price"] if act2 else 0,
    ])

    return {
        "destinationName": f"{itinerary['origin']} → {city1} & {city2}",
        "totalPrice": str(total),
        "description": (
            f"Personalized trip from {itinerary['origin']} to {city1} and {city2}, "
            f"tailored to your budget and travel style."
        ),
        "picture": "",
        "destinationsList": [
            {
                "name": city1,
                "transportation": [t for t in [to_transport(leg1)] if t],
                "cities": [{
                    "name": city1,
                    "country": city1,
                    "accommodation": to_acc(acc1),
                    "activityDetails": to_activity(act1)
                }]
            },
            {
                "name": city2,
                "transportation": [t for t in [to_transport(leg2), to_transport(leg3)] if t],
                "cities": [{
                    "name": city2,
                    "country": city2,
                    "accommodation": to_acc(acc2),
                    "activityDetails": to_activity(act2)
                }]
            }
        ]
    }


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    execute_pipeline()
    itinerary = build_smart_itinerary()

    if itinerary:
        accommodations = build_smart_accommodation(itinerary)
        activities = build_smart_activity(itinerary)
        package = build_package(itinerary, accommodations, activities)

        output_path = "output/package.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(package, f, indent=2)

        print(json.dumps(package, indent=2))
        print(f"\n✅ Package saved to {output_path}")
