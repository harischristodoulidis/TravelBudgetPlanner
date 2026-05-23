import pandas as pd
import json
import io
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# ==========================================
# 1. TRAIN THE OFFLINE NLP AGENT 
# ==========================================
# Expanded training data to cover the vendors found in the CSV.
training_data = [
    # Income & Interest
    ("ΕΙΣΕΡΧΟΜΕΝΟ ΕΜΒΑΣΜΑ CREDIT TRANSFER", "Income"),
    ("ΜΕΤΑΦΟΡΑ ΥΠΟΛΟΙΠΟΥ - ΜΕΤΑΠΤΩΣΗ", "Income"),
    ("ΤΟΚΟΙ ΚΑΤΑΘΕΣΕΩΝ ΣΕ ΛΟΓΑΡΙΑΣΜΟΥΣ ΕΥΡΩ", "Income"),
    ("ΤΟΚΟΙ ΤΑΜΙΕΥΤΗΡΙΟΥ", "Income"),
    
    # Supermarkets & Groceries
    ("SKLAVENITIS IOANNINA ΑΝΑΛΗΨΗ ΓΙΑ ΑΓΟΡΕΣ", "Supermarket"),
    ("DIAMANTIS MASOUTIS SA ΑΝΑΛΗΨΗ ΓΙΑ", "Supermarket"),
    ("AB_IOANNINA_ANATOLI", "Supermarket"),
    ("AB VASILOPOULOS S.A.", "Supermarket"),
    ("MARKET IN", "Supermarket"),
    ("MY MARKET", "Supermarket"),
    ("GALAKTOCOMICA DIMITRIOU", "Supermarket"),
    ("TIROK. KOSTARELOU", "Supermarket"),
    ("SUPERMARKET PAPAGEOR", "Supermarket"),
    
    # Dining, Fast Food & Cafes
    ("PIATSA TILIXTO PANOR", "Dining_Cafes"),
    ("MIKEL", "Dining_Cafes"),
    ("BRUNO", "Dining_Cafes"),
    ("DETOX", "Dining_Cafes"),
    ("O MPOTSARHS", "Dining_Cafes"),
    ("KAVOURAS", "Dining_Cafes"),
    
    # Cars & Gas
    ("EKO TSILIKIS ALEXIOU", "Gas_Station"),
    ("EKO M&P KASI OE", "Gas_Station"),
    ("SHELL KITSOGLOU", "Gas_Station"),
    ("MYRTEA AE", "Gas_Station"),
    
    # Public Transit
    ("YPERASTIKO KTEL IOAN", "Public_Transit"),
    ("YPER  KTEL N  IOANNINON", "Public_Transit"),
    
    # Sports & Active
    ("ATILOS SPORT MONOPROSOPI", "Sports_Active"),
    ("ZACKRET", "Sports_Active"),
    ("HALL OF BRANDS", "Sports_Active"),
    ("ADMIRAL", "Sports_Active"),
    
    # Tech & Electronics
    ("PUBLIC IOANNINA", "Electronics_Tech"),
    ("GERMANOS", "Electronics_Tech"),
    ("DIXONS-KOTSOVOLOS", "Electronics_Tech"),
    ("WELCOME STORES ILEKTRAGOR", "Electronics_Tech"),
    
    # Home, DIY & Outdoors
    ("PRAKTIKER HELLAS", "Home_DIY"),
    ("PORCELANA", "Home_DIY"),
    ("STROM ECO", "Home_DIY"),
    ("LABROU CERAMICS", "Home_DIY"),
    ("CHILIA AROMATA", "Home_DIY"),
    
    # Other
    ("FUNKY BUDDHA", "Clothing_Shopping"),
    ("EL CORTE INGLES SA", "International_Travel"),
    ("BAVARIAN SKY", "International_Travel"),
    ("OPAP", "Betting_Nightlife"),
    ("qkHPzMH kOc/sMOY dEH", "Utilities_Bills"),
    ("DEIAI", "Utilities_Bills"),
    ("ΑΝΑΛΗΨΗ ΑΠΟ ATM", "ATM_Cash"),
    ("ΑΝΑΛΗΨΗ  ΜΕΤΡΗΤΩΝ", "ATM_Cash"),
    ("FARMAKEIO", "Pharmacy_Health"),
    ("ELTA ELLHNIKOY", "Post_Courier"),
    ("ACS IOANNINA", "Post_Courier")
]

X_train = [item[0] for item in training_data]
y_train = [item[1] for item in training_data]

# Train the NLP Model
nlp_agent = make_pipeline(CountVectorizer(ngram_range=(1, 3)), MultinomialNB())
nlp_agent.fit(X_train, y_train)

# ==========================================
# 2. THE PROFILING ALGORITHM
# ==========================================
def clean_european_amounts(val) -> float:
    """Converts European numbers like '-2.000,00' or '-53.06' to standard Python floats."""
    if isinstance(val, str):
        val = val.replace('"', '').strip() # Remove quotes
        # If it has both dots and commas (e.g. 2.000,00), remove the dot, change comma to dot
        if '.' in val and ',' in val:
            val = val.replace('.', '').replace(',', '.')
        # If it only has a comma (e.g. 53,06), change it to dot
        elif ',' in val:
            val = val.replace(',', '.')
    return float(val)

def process_user_transactions(csv_string: str, user_id: str) -> str:
    """Reads the CSV, uses NLP to categorize, and outputs the 1-10 JSON profile."""
    
    # 1. Clean the CSV (Remove the "Username:" line so pandas doesn't crash)
    clean_csv_lines = [line for line in csv_string.strip().split('\n') if "Username:" not in line and line.strip() != ""]
    clean_csv_string = "\n".join(clean_csv_lines)
    
    # 2. Load into Pandas
    df = pd.read_csv(io.StringIO(clean_csv_string), header=None, 
                     names=["Timestamp", "Account", "Description", "Amount", "Currency"])
    
    # Apply our European amount cleaner
    df['Amount'] = df['Amount'].apply(clean_european_amounts)
    
    # Parse Dates and calculate the total span of the data in MONTHS
    df['Datetime'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S')
    df['Date'] = df['Datetime'].dt.date
    df['Hour'] = df['Datetime'].dt.hour
    
    # Calculate how many months of data this CSV contains (Minimum 1 to avoid division by zero)
    days_active = (df['Date'].max() - df['Date'].min()).days
    months_of_data = max(1.0, days_active / 30.44)
    
    # 3. Ask the NLP Agent to predict the category of every transaction
    df['Category'] = nlp_agent.predict(df['Description'])
    
    # 4. Aggregate data for math logic
    total_txns = max(1, len(df))
    total_income = df[df['Category'] == 'Income']['Amount'].sum()
    total_spend = abs(df[df['Amount'] < 0]['Amount'].sum())
    spend_by_cat = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().abs().to_dict()
    
    def get_spend(cat): return spend_by_cat.get(cat, 0.0)

    # -----------------------------------------------------
    # 3. CALCULATE THE 1-10 SCORES (Using Monthly Averages)
    # -----------------------------------------------------
    def clamp(val): return int(max(1, min(10, round(val))))

    # A. Spending Power
    monthly_income = total_income / months_of_data
    budget_capacity = clamp((monthly_income / 300) + 1) 
    
    supermarket_ratio = get_spend('Supermarket') / max(1, total_spend)
    price_sensitivity = clamp(1 + (supermarket_ratio * 15))

    # B. Experience Preferences
    food_spend = get_spend('Dining_Cafes') + get_spend('Supermarket') + 1
    dining_sophistication = clamp(1 + ((get_spend('Dining_Cafes') / food_spend) * 15))
    
    cultural_engagement = clamp(3) # Hardcoded low as no clear culture transactions exist in this DB
    
    # Nightlife mixes OPAP/Betting spend with late night transactions
    late_night_txns = df[(df['Hour'] >= 21) | (df['Hour'] <= 4)].shape[0]
    late_night_ratio = late_night_txns / total_txns
    monthly_betting = get_spend('Betting_Nightlife') / months_of_data
    nightlife_propensity = clamp(1 + (late_night_ratio * 30) + (monthly_betting / 20))
    
    active_days_per_month = df['Date'].nunique() / months_of_data
    pace_and_goal = clamp(active_days_per_month / 1.5) 

    # C. Movement & Geography
    monthly_transit = get_spend('Public_Transit') / months_of_data
    monthly_gas = get_spend('Gas_Station') / months_of_data
    
    if monthly_transit > monthly_gas:
        mobility_style = clamp(4 - (monthly_transit / 10)) # Heavy bus user = lower score
    else:
        mobility_style = clamp(5 + (monthly_gas / 30))     # Heavy gas user = higher score
    
    monthly_international = get_spend('International_Travel') / months_of_data
    geo_orientation = clamp(3 + (monthly_international / 20))

    # D. Lifestyle Signals
    monthly_sports = get_spend('Sports_Active') / months_of_data
    physical_activity = clamp(1 + (monthly_sports / 15))
    
    monthly_diy = get_spend('Home_DIY') / months_of_data
    nature_values = clamp(3 + (monthly_diy / 20))

    # -----------------------------------------------------
    # 4. BUILD THE JSON OUTPUT
    # -----------------------------------------------------
    profile_json = {
        "user_id": user_id,
        "user_travel_profile": {
            "spending_power": {
                "budget_capacity": budget_capacity,
                "price_sensitivity": price_sensitivity
            },
            "experience_preferences": {
                "dining_sophistication": dining_sophistication,
                "cultural_engagement": cultural_engagement,
                "nightlife_propensity": nightlife_propensity,
                "pace_and_goal": pace_and_goal
            },
            "movement_and_geography": {
                "mobility_style": mobility_style,
                "geographic_orientation": geo_orientation
            },
            "lifestyle_signals": {
                "physical_activity_level": physical_activity,
                "nature_and_values": nature_values
            }
        }
    }
    
    return json.dumps(profile_json, indent=2)

# ==========================================
# 3. RUN THE CODE (COMMAND LINE INTERFACE)
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate user travel profile from transactions CSV.")
    parser.add_argument("csv_path", help="Path to transactions CSV file.")
    parser.add_argument("--user-id", default="user_1", help="User id to include in the profile JSON.")
    parser.add_argument("--output", default="testing_user_from_csv.json", help="Output JSON file path.")
    args = parser.parse_args()

    # Read CSV file contents
    try:
        with open(args.csv_path, "r", encoding="utf-8") as f:
            csv_string = f.read()
            
        # Process and produce profile JSON
        result_json = process_user_transactions(csv_string, args.user_id)

        # Write JSON to output file
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_json)

        print(f"Success! Generated profile saved to {args.output}")
        
    except FileNotFoundError:
        print(f"Error: The file '{args.csv_path}' was not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")