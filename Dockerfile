# התחל עם אימג' רשמי של פייתון
FROM python:3.10-slim

# התקנת תלויות מערכת (כרום וכל מה שצריך)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    # הוספת המפתח של גוגל כרום
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    # הוספת המקור של כרום
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    # התקנת כרום
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # ניקוי
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
