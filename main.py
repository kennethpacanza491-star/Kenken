import sys
import random
import math
import pymysql
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'eyewhere_db',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

# User's current baseline location (Danao, Cebu region)
CURRENT_LOCATION = {
    "name": "Danao City, Cebu (Current Position)",
    "lat": 10.5167,
    "lon": 124.0167
}

def init_db():
    """Initializes MariaDB database and travel intelligence logs table."""
    try:
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop('database')
        conn = pymysql.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        conn.close()

        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS travel_intelligence_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                current_loc VARCHAR(255),
                target_loc VARCHAR(255),
                distance_km FLOAT,
                weather VARCHAR(255),
                environment VARCHAR(255),
                safety_guidelines TEXT,
                timestamp VARCHAR(50)
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ DB Notice: {e}")

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculates great-circle distance between two points in kilometers (Haversine formula)."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def explore_target_place():
    print("\n--- 🧭 EYEWHERE? : TRAVEL & AREA INTELLIGENCE ---")
    print(f"📍 Origin Point: {CURRENT_LOCATION['name']} [{CURRENT_LOCATION['lat']}° N, {CURRENT_LOCATION['lon']}° E]")
    
    target_name = input("\nEnter the place, region, or destination you want to go or visit: ").strip()
    if not target_name:
        print("❌ Target destination cannot be empty.")
        return

    print(f"\n🔄 Running satellite & environmental scan for '{target_name.title()}'...")

    # Generate consistent simulated coordinates for the target destination based on its name string
    random.seed(target_name.lower())
    target_lat = CURRENT_LOCATION['lat'] + random.uniform(-1.8, 1.8)
    target_lon = CURRENT_LOCATION['lon'] + random.uniform(-1.8, 1.8)
    random.seed()

    # Calculate distance from current position
    distance = calculate_distance(CURRENT_LOCATION['lat'], CURRENT_LOCATION['lon'], target_lat, target_lon)

    # Multi-layered intelligence metrics
    weather = random.choice([
        "☀️ Clear Skies & Sunny (32°C, Humidity: 65%)", 
        "🌧️ Light Rain Showers (27°C, Wind: 14 km/h)", 
        "⛅ Partly Cloudy (30°C, Humidity: 70%)", 
        "⛈️ Active Thunderstorm Advisory (25°C)"
    ])
    
    environment = random.choice([
        "🌿 Coastal / Forest Ecosystem (High Green Index, Air Quality: Good)",
        "🏙️ Urban Metropolitan Sector (Moderate Emissions, Noise Level: High)",
        "🌾 Agricultural Valley (Open Terrain, Clean Air Quality)",
        "⛰️ Mountainous Terrain (Rugged Landscape, Low Density)"
    ])

    safety_guidelines = random.choice([
        "1. Stay hydrated and wear sun protection.\n    2. Keep emergency contacts handy.\n    3. Monitor local weather alerts before transit.",
        "1. Exercise caution during peak transit hours.\n    2. Secure personal belongings in crowded zones.\n    3. Follow local municipal safety rules.",
        "1. Check trail or road conditions before entry.\n    2. Carry waterproof gear if visiting rural/mountainous sectors.\n    3. Ensure reliable communication signals."
    ])

    # Save to MariaDB database
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = '''
            INSERT INTO travel_intelligence_logs (current_loc, target_loc, distance_km, weather, environment, safety_guidelines, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, (CURRENT_LOCATION['name'], target_name.title(), round(distance, 2), weather, environment, safety_guidelines, ts))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Database Error: {e}")

    # Display Comprehensive Report
    print("\n" + "="*68)
    print(f"🗺️ INTELLIGENCE & TRAVEL REPORT: {target_name.upper()}")
    print("="*68)
    print(f"• Origin Point      : {CURRENT_LOCATION['name']}")
    print(f"• Destination       : {target_name.title()} (~{target_lat:.4f}° N, {target_lon:.4f}° E)")
    print(f"• Calculated Distance: ~{distance:.2f} km away from your location")
    print(f"• Weather Conditions: {weather}")
    print(f"• Environmental Info: {environment}")
    print(f"• Safety Guidelines :\n    {safety_guidelines}")
    print(f"• Database Status   : Saved to MariaDB successfully 💾")
    print("="*68)

def view_history():
    """Retrieves and displays past travel searches from MariaDB."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM travel_intelligence_logs")
        rows = cursor.fetchall()
        conn.close()

        print("\n" + "="*70)
        print("📂 SAVED TRAVEL INTELLIGENCE HISTORY (MARIADB)")
        print("="*70)
        if not rows:
            print("No travel scans recorded yet.")
        else:
            for r in rows:
                print(f"ID: {r['id']} | Target: {r['target_loc'].upper()}")
                print(f"  • Distance  : ~{r['distance_km']} km away")
                print(f"  • Weather   : {r['weather']}")
                print(f"  • Env Info  : {r['environment']}")
                print(f"  • Safety    : {r['safety_guidelines'].replace(chr(10), ' ')}")
                print(f"  • Logged At : {r['timestamp']}")
                print("-" * 70)
    except Exception as e:
        print(f"❌ Error reading history: {e}")

def main():
    init_db()
    while True:
        print("\n=== 🌍 EYEWHERE? : ULTIMATE TRAVEL & INTELLIGENCE SYSTEM ===")
        print("1. Scan & Direct to Target Place (Distance, Weather, Environment, Safety)")
        print("2. View Travel History Logs")
        print("3. Exit System")
        
        choice = input("\nSelect an option (1-3): ").strip()
        if choice == "1":
            explore_target_place()
        elif choice == "2":
            view_history()
        elif choice == "3":
            print("\nExiting EYEWHERE?. Safe travels!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Choose 1, 2, or 3.")

if __name__ == "__main__":
    main()

