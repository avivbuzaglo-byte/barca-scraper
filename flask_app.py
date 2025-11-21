from flask import Flask, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app) 

# --- מחקנו את כל הפונקציות של SELENIUM ---

@app.route('/get_player_stats')
def get_player_stats():
    # --- הוספנו לוג ---
    print("\n--- NEW REQUEST: /get_player_stats received ---")
    
    # --- החזרת JSON מזויף באופן מיידי ---
    # (בלי Selenium, בלי שום דבר כבד)
    player_data = {
        "name": "Lamine Yamal (Dummy)",
        "number": "#27",
        "goals": "10",
        "assists": "5"
    }
    
    print("--- Sending DUMMY JSON response. ---")
    return jsonify(player_data)

# --- הרצת השרת (חשוב ל-Render) ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"--- Flask App (Dummy Version) Starting on port {port} ---")
    app.run(host='0.0.0.0', port=port)
