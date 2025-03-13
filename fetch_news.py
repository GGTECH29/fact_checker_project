import requests
import pandas as pd
import sys

# API-Schlüssel und URL
api_key = "a4f79e5cf97843c0b420e893108a8fb5"  # Ersetze dies durch deinen API-Schlüssel
url = f"https://newsapi.org/v2/top-headlines?country=de&category=technology&apiKey={api_key}"

try:
    # Sende eine Anfrage an die API
    response = requests.get(url)
    response.raise_for_status()  # Wirft eine Ausnahme bei HTTP-Fehlern

    # Überprüfe, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        data = response.json()
        print("API-Antwort:", data)  # Debug-Ausgabe
        articles = data.get("articles", [])
        if not articles:
            print("Keine Artikel gefunden.")
            sys.exit()  # Beende das Skript, falls keine Artikel vorhanden sind

        # Erstelle eine Liste mit den relevanten Daten
        data = []
        for article in articles:
            title = article.get("title", "Kein Titel verfügbar")
            description = article.get("description", "Keine Beschreibung verfügbar")
            url = article.get("url", "Keine URL verfügbar")
            source = article.get("source", {}).get("name", "Unbekannte Quelle")
            data.append({"title": title, "description": description, "url": url, "source": source})

        # Erstelle einen DataFrame
        df = pd.DataFrame(data)

        # Speichere die Daten in einer CSV-Datei
        df.to_csv("german_news.csv", index=False, encoding="utf-8-sig")
        print("Daten gespeichert in german_news.csv")
    else:
        print(f"Fehler bei der Anfrage: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Fehler bei der Anfrage: {e}")