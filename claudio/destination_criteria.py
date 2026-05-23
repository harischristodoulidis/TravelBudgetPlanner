def generate_travel_parameters(user_profile: dict) -> dict:
    """
    Takes a dictionary of user profile scores (1-10) and calculates
    actionable search parameters for a travel application.
    """
    
    # ---------------------------------------------------------
    # 1. DESTINATION (Cities) -> destination_affinity_index
    # Output: 1-10 scores matching the user to specific city archetypes
    # ---------------------------------------------------------
    # Note: Random values
    # (e.g., 10/10 budget_capacity = 1/10 affinity for a budget city)
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
    # Divided by 1.50 to normalize the custom weights back to a 1-10 scale
    trans_index = (
        (user_profile["budget_capacity"] * 0.70) + 
        (user_profile["mobility_style"] * 0.40) + 
        (user_profile["pace_and_goal"] * 0.40)
    ) / 1.50
    
    # ---------------------------------------------------------
    # 3. ACCOMMODATION (Where to stay) -> acc_tier_index
    # Output: 1 to 10 scale representing the star rating/luxury tier
    # ---------------------------------------------------------
    # Divided by 1.40 to normalize the custom weights back to a 1-10 scale
    acc_tier_index = (
        (user_profile["budget_capacity"] * 0.70) + 
        (user_profile["price_sensitivity"] * 0.30) + 
        (user_profile["dining_sophistication"] * 0.40)
    ) / 1.40
    
    # ---------------------------------------------------------
    # 4. ACTIVITIES & EVENTS (What to do) -> activities_index
    # Output: 1-10 scores representing the demand/intensity for each activity type
    # ---------------------------------------------------------
    # The weights sum to 1.00, so the result naturally stays on a 1-10 scale.
    
    # Mixes culture interest with how busy they want the trip to be (pace)
    culture_index = (user_profile["cultural_engagement"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    
    # Mixes sports interest with how busy they want the trip to be
    sports_index = (user_profile["physical_activity_level"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    
    # Mixes partying interest with how busy they want the trip to be
    nightlife_index = (user_profile["nightlife_propensity"] * 0.70) + (user_profile["pace_and_goal"] * 0.30)
    
    # Mixes food interest with what they can actually afford to spend on dining
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


import math

def calculate_city_match(user_affinity, city_profile):
    """
    Calculates how well a city matches the user's destination affinity.
    Returns the Euclidean distance and a 0-100% match score.
    """
    
    # 1. Define the keys we are comparing
    keys = ["budget_city", "relaxed_city", "natural_city", "cultural_city", "nightlife_city"]
    
    # 2. Calculate the sum of squared differences (Euclidean Distance math)
    sum_of_squares = 0
    for key in keys:
        difference = user_affinity[key] - city_profile[key]
        sum_of_squares += (difference ** 2)
        
    distance = math.sqrt(sum_of_squares)
    
    # 3. Convert distance to a 100% Match Score
    # The maximum possible distance between two 1-10 scales across 5 variables is ~20.12
    # Math: sqrt((10-1)^2 * 5) = sqrt(81 * 5) = sqrt(405) = 20.124
    max_possible_distance = 20.124
    
    match_percentage = 100 - ((distance / max_possible_distance) * 100)
    
    return {
        "distance": round(distance, 2),
        "match_percentage": round(match_percentage, 1)
    }

# ==========================================
# EXAMPLE USAGE / TEST
# ==========================================
if __name__ == "__main__":
    # Mock data outputted by your bank transaction parser (1-10 scale)
    mock_user_path = "testing_user.json"
    import json

    with open(mock_user_path, "r") as f:
        mock_user = json.load(f)

    if "user_travel_profile" in mock_user:
        profile = mock_user["user_travel_profile"]
        flat_profile = {}
        for section in [
            "spending_power",
            "experience_preferences",
            "movement_and_geography",
            "lifestyle_signals"
        ]:
            if section in profile and isinstance(profile[section], dict):
                flat_profile.update(profile[section])
        mock_user = flat_profile


    ########################################################################################
    ## MOCK CITY PROFILES (1-10 scale)
    city_1=  {
    "budget_city": 8,
    "relaxed_city": 5,
    "natural_city": 8,
    "cultural_city": 9,
    "nightlife_city": 2
    }

    city_2=  {
        "budget_city": 2,
        "relaxed_city": 5,
        "natural_city": 4,
        "cultural_city": 3,
        "nightlife_city": 9
    }
    ########################################################################################

    results = generate_travel_parameters(mock_user)
    
    print("user profile:\n" + json.dumps(mock_user, indent=4)+ "\n")
    print("travel parameters:\n" + json.dumps(results, indent=4))
    
    print()
    print()
    score_city_1 = calculate_city_match(results["destination_affinity_index"], city_1)
    score_city_2 = calculate_city_match(results["destination_affinity_index"], city_2)

    print(f"City 1 Match: {score_city_1['match_percentage']}% (Distance: {score_city_1['distance']})")
    print(f"City 2 Match: {score_city_2['match_percentage']}% (Distance: {score_city_2['distance']})")