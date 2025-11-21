# התחל עם אימג' רשמי של פייתון
FROM python:3.10-slim

# הגדרת משתני סביבה כדי למנוע שאלות אינטראקטיביות
ENV DEBIAN_FRONTEND=noninteractive

# התקנת תלויות מערכת (כרום וכל מה שצריך)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # 1. הורדת המפתח של גוגל
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > google.pub \
    # 2. המרת המפתח לפורמט gpg ושמירתו במקום הנכון (במקום apt-key)
    && gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg google.pub \
    # 3. ניקוי המפתח שהורדנו
    && rm google.pub \
    # 4. הוספת המקור של כרום *עם חתימה למפתח הנכון*
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    # 5. התקנת כרום
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # 6. ניקוי
    && rm -rf /var/lib/apt/lists/*

# הגדרת תיקיית עבודה
WORKDIR /app

# העתקת קובץ הדרישות
COPY requirements.txt requirements.txt

# התקנת ספריות הפייתון
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר קוד האפליקציה
COPY . .

# הפקודה להרצת האפליקציה כשהשרת עולה
CMD ["python", "flask_app.py"]
