from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os # נייבא את os כדי לקרוא את הפורט

app = Flask(__name__)
CORS(app) 

def setup_driver():
    options = webdriver.ChromeOptions()
    # הגדרות חובה לריצה בשרת לינוקס (כמו Render)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless") # ריצה ברקע
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080") # גודל חלון סטנדרטי
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # שימוש ב-webdriver-manager להתקנה אוטומטית של הדרייבר הנכון
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    return driver

@app.route('/get_player_stats')
def get_player_stats():
    
    # --- URL קבוע לבדיקה ---
    url_to_scrape = "https://www.espn.com/soccer/player/stats/_/id/382062/lamine-yamal"
    
    driver = setup_driver()
    player_data = {} 

    try:
        driver.get(url_to_scrape)
        
        # --- איתור הנתונים ---
        # נחכה עד שהדף ייטען ונמצא את שם השחקן
        # (ה-Selector הזה נכון ל-ESPN נכון לכתיבת שורות אלה)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".PlayerHeader__Name"))
        )

        # חילוץ שם ומספר
        player_name = driver.find_element(By.CSS_SELECTOR, ".PlayerHeader__Name").text
        player_number = driver.find_element(By.CSS_SELECTOR, ".PlayerHeader__Jersey").text

        # חילוץ סטטיסטיקות (דוגמה)
        # נצטרך למצוא את הסלקטורים המדויקים לטבלה
        # למשל (זה ניחוש!):
        # goals = driver.find_element(By.XPATH, "//span[text()='Goals']/following-sibling::span").text
        # assists = driver.find_element(By.XPATH, "//span[text()='Assists']/following-sibling::span").text

        player_data = {
            "name": player_name,
            "number": player_number,
            "goals": "N/A", # נעדכן כשנמצא סלקטור
            "assists": "N/A" # נעדכן כשנמצא סלקטור
        }

    except Exception as e:
        # אם הסקריפינג נכשל
        player_data = {"error": str(e)}
        
    finally:
        driver.quit() # סגירת הדפדפן

    return jsonify(player_data)

# --- הרצת השרת (חשוב ל-Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
