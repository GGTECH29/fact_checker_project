import pandas as pd
import os
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Verzeichnis überprüfen
data_dir = "data"
if not os.path.exists(data_dir):
    logging.error(f"Fehler: Das Verzeichnis '{data_dir}' existiert nicht.")
    sys.exit(1)

# CSV-Dateien laden
csv_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".csv")]
if not csv_files:
    logging.error(f"Fehler: Das Verzeichnis '{data_dir}' enthält keine CSV-Dateien.")
    sys.exit(1)

# Daten zusammenführen
dfs = []
for file in csv_files:
    try:
        df = pd.read_csv(file)
        dfs.append(df)
        logging.info(f"Datei '{file}' erfolgreich geladen.")
    except Exception as e:
        logging.error(f"Fehler beim Laden der Datei '{file}': {e}")

if not dfs:
    logging.error("Keine Daten zum Zusammenführen gefunden.")
    sys.exit(1)

df_combined = pd.concat(dfs, ignore_index=True)

# Daten speichern
try:
    df_combined.to_csv("combined_data.csv", index=False)
    logging.info("Daten erfolgreich zusammengeführt und gespeichert.")
except Exception as e:
    logging.error(f"Fehler beim Speichern der Daten: {e}")
    sys.exit(1)
