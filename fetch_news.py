import requests
import pandas as pd
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API-Schlüssel und URL
api_key = "a4f79e5cf97843c0b420e893108a8fb5"  # Ersetze dies durch deinen API-Schlüssel
url = f"https://newsapi.org/v2/top-headlines?country=de&apiKey={api_key}"

# API-Anfrage senden
try:
    response = requests.get(url)
    response.raise_for_status()
    logging.info("API-Anfrage erfolgreich.")
except requests.exceptions.RequestException as e:
    logging.error(f"Fehler bei der API-Anfrage: {e}")
    sys.exit(1)

# Daten verarbeiten
data = response.json()
if "articles" not in data:
    logging.error("Fehler: Die API-Antwort enthält keine Artikel.")
    sys.exit(1)

articles = data["articles"]
if not articles:
    logging.warning("Keine Artikel gefunden.")
    sys.exit(0)

# Daten extrahieren
news_data = []
for article in articles:
    title = article.get("title", "Kein Titel verfügbar")
    description = article.get("description", "Keine Beschreibung verfügbar")
    url = article.get("url", "Keine URL verfügbar")
    source = article.get("source", {}).get("name", "Unbekannte Quelle")
    news_data.append({"title": title, "description": description, "url": url, "source": source})

# DataFrame erstellen und speichern
df = pd.DataFrame(news_data)
try:
    df.to_csv("german_news.csv", index=False)
    logging.info("Daten erfolgreich gespeichert.")
except Exception as e:
    logging.error(f"Fehler beim Speichern der Daten: {e}")
    sys.exit(1)
