import math
import json

def generate_travel_parameters(user_profile: dict) -> dict:
    """
    Takes a dictionary of user profile scores (1-10) and calculates
    actionable search parameters for a travel application.
    """
    
    # ---------------------------------------------------------
    # 1. DESTINATION (Cities) -> destination_affinity_index
    # Output: 1-10 scores matching the user to specific city archetypes
    # ---------------------------------------------------------
    destination_affinity_index = {
        "budget_city": round(user_profile["budget_capacity"] * 0.90, 2),
        "relaxed_city": round(user_profile["pace_and_goal"] * 0.70, 2),
        "natural_city": round(user_profile["nature_and_values"] * 0.70, 2),
        "cultural_city": round(user_profile["cultural_engagement"] * 0.90, 2),
        "nightlife_city": round(user_profile["nightlife_propensity"] * 0.70, 2)
    }

    # ---------------------------------------------------------
    # 2. TRANSPORTATION (Long-distance & Intercity) -> trans_index
    # Output: 1 to 10 scale (1 = Budget/Slow, 10 = Premium/Fast)
    # ---------------------------------------------------------
    trans_index = (
        (user_profile["budget_capacity"] * 0.70) + 
        (user_profile["mobility_style"] * 0.40) + 
        (user_profile["pace_and_goal"] * 0.40)
    ) / 1.50
    
    # ---------------------------------------------------------
    # 3. ACCOMMODATION (Where to stay) -> acc_tier_index
    # Output: 1 to 10 scale representing the star rating/luxury tier
    # ---------------------------------------------------------
    acc_tier_index = (
        (user_profile["budget_capacity"] * 0.70) + 
        (user_profile["price_sensitivity"] * 0.30) + 
        (user_profile["dining_sophistication"] * 0.40)
    ) / 1.40
    
    # ---------------------------------------------------------
    # 4. ACTIVITIES & EVENTS (What to do) -> activities_index
    # Output: 1-10 scores representing the demand/intensity for each activity type
    # ---------------------------------------------------------
    culture_index = (user_profile["cultural_engagement"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    sports_index = (user_profile["physical_activity_level"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    nightlife_index = (user_profile["nightlife_propensity"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    food_index = (user_profile["dining_sophistication"] * 0.70) + (user_profile["budget_capacity"] * 0.30)

    activities_index = {
        "culture_index": round(culture_index, 2),
        "sports_index": round(sports_index, 2),
        "nightlife_index": round(nightlife_index, 2),
        "food_index": round(food_index, 2)
    }

    return {
        "destination_affinity_index": destination_affinity_index,
        "trans_index": round(trans_index, 2),
        "acc_tier_index": round(acc_tier_index, 2),
        "activities_index": activities_index
    }

def calculate_city_match(user_affinity, city_profile):
    """
    Calculates how well a city matches the user's destination affinity.
    Returns the Euclidean distance and a 0-100% match score.
    """
    keys = ["budget_city", "relaxed_city", "natural_city", "cultural_city", "nightlife_city"]
    
    sum_of_squares = 0
    for key in keys:
        # Default to 5.0 if a key is missing for some reason
        user_val = user_affinity.get(key, 5.0)
        city_val = city_profile.get(key, 5.0)
        
        difference = user_val - city_val
        sum_of_squares += (difference ** 2)
        
    distance = math.sqrt(sum_of_squares)
    max_possible_distance = 20.124
    match_percentage = 100 - ((distance / max_possible_distance) * 100)
    
    return {
        "distance": round(distance, 2),
        "match_percentage": round(match_percentage, 1)
    }

# ==========================================
# MAIN EXECUTION
# ==========================================
def create_destination_leaderboard():
    
    # 1. LOAD USER PROFILE
    user_path = "output/user_profile.json"
    try:
        with open(user_path, "r") as f:
            user = json.load(f)
            
        if "user_travel_profile" in user:
            profile = user["user_travel_profile"]
            flat_profile = {}
            for section in ["spending_power", "experience_preferences", "movement_and_geography", "lifestyle_signals"]:
                if section in profile and isinstance(profile[section], dict):
                    flat_profile.update(profile[section])
            user = flat_profile
            
    except FileNotFoundError:
        print(f"Error: {user_path} not found.")
        exit()

    # Generate user travel parameters
    results = generate_travel_parameters(user)
        
    # 2. LOAD REAL CITY PROFILES
    city_path = "mock/city_profiles.json"
    try:
        with open(city_path, "r") as f:
            cities_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {city_path} not found. Make sure you generated it first!")
        exit()

    # 3. CALCULATE MATCHES FOR ALL CITIES
    match_results = []
    
    for city_name, city_profile in cities_data.items():
        score = calculate_city_match(results["destination_affinity_index"], city_profile)
        
        match_results.append({
            "city": city_name,
            "match_percentage": score["match_percentage"],
            "distance": score["distance"]
        })
        
    # Sort the results so the best match is at the top
    match_results = sorted(match_results, key=lambda x: x["match_percentage"], reverse=True)

    # 4. PRINT FINAL LEADERBOARD
    for rank, match in enumerate(match_results, 1):
        print(f"{rank}. {match['city']:<10} | Match: {match['match_percentage']}%  (Distance: {match['distance']})")

if __name__ == "__main__":
    create_destination_leaderboard()