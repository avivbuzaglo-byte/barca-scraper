from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time # נייבא את time כדי למדוד זמנים

app = Flask(__name__)
CORS(app) 

def setup_driver():
    # --- הוספנו לוגים ---
    print("--- Starting setup_driver() ---")
    start_time = time.time()
    
    options = webdriver.ChromeOptions()
    print("Setting Chrome options...")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    print("Installing/Finding Chrome Driver...")
    s = Service(ChromeDriverManager().install())
    
    print("Initializing webdriver.Chrome()...")
    driver = webdriver.Chrome(service=s, options=options)
    
    end_time = time.time()
    print(f"--- Driver setup complete. Took {end_time - start_time:.2f} seconds ---")
    return driver

@app.route('/get_player_stats')
def get_player_stats():
    # --- הוספנו לוגים ---
    print("\n--- NEW REQUEST: /get_player_stats received ---")
    
    url_to_scrape = "https://www.espn.com/soccer/player/stats/_/id/382062/lamine-yamal"
    driver = None # נאתחל כ-None
    player_data = {} 

    try:
        print("Step 1: Setting up driver...")
        driver = setup_driver()
        print("Step 1 Complete.")

        print(f"Step 2: Attempting to get URL: {url_to_scrape}")
        driver.get(url_to_scrape)
        print("Step 2 Complete. Page loaded.")

        print("Step 3: Waiting for element '.PlayerHeader__Name'...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".PlayerHeader__Name"))
        )
        print("Step 3 Complete. Element found.")

        print("Step 4: Scraping data...")
        player_name = driver.find_element(By.CSS_SELECTOR, ".PlayerHeader__Name").text
        player_number = driver.find_element(By.CSS_SELECTOR, ".PlayerHeader__Jersey").text

        player_data = {
            "name": player_name,
            "number": player_number,
            "goals": "N/A", 
            "assists": "N/A"
        }
        print("Step 4 Complete. Data scraped.")

    except Exception as e:
        # אם הסקריפינג נכשל
        print(f"---!!! SCRIPT CRASHED !!!---")
        print(str(e)) # נדפיס את השגיאה ללוג
        player_data = {"error": str(e)}
        
    finally:
        if driver:
            print("Step 5: Quitting driver...")
            driver.quit() 
            print("Step 5 Complete. Driver quit.")
        
    print("--- REQUEST FINISHED. Sending JSON response. ---")
    return jsonify(player_data)

# --- הרצת השרת (חשוב ל-Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"--- Flask App Starting on port {port} ---")
    app.run(host='0.0.0.0', port=port)
