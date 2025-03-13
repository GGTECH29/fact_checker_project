import pandas as pd
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Daten laden
try:
    df = pd.read_csv("news_sample.csv")
    logging.info("Daten erfolgreich geladen.")
except FileNotFoundError:
    logging.error("Fehler: Die Datei 'news_sample.csv' wurde nicht gefunden.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    logging.error("Fehler: Die Datei 'news_sample.csv' ist leer oder enthält keine gültigen Daten.")
    sys.exit(1)

# Überprüfen, ob die erforderlichen Spalten vorhanden sind
required_columns = ["title", "content", "type"]
if not all(column in df.columns for column in required_columns):
    logging.error("Fehler: Die CSV-Datei enthält nicht alle erforderlichen Spalten.")
    sys.exit(1)

# Daten bereinigen
df = df[["title", "content", "type"]]
df.columns = ["title", "text", "is_fake"]

# Daten speichern
try:
    df.to_csv("clean_fake_news.csv", index=False)
    logging.info("Daten erfolgreich bereinigt und gespeichert.")
except Exception as e:
    logging.error(f"Fehler beim Speichern der Daten: {e}")
    sys.exit(1)
