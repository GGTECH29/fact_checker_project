import pandas as pd
import os

# Pfad zum Datenordner
data_dir = "data"

# Liste aller .txt-Dateien im Datenordner
txt_files = []
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".txt"):
            txt_files.append(os.path.join(root, file))

# Lade alle .txt-Dateien
dfs = []
for file in txt_files:
    try:
        # Versuche, die Datei mit verschiedenen Trennzeichen zu laden
        try:
            # Versuche Tabulator als Trennzeichen
            df = pd.read_csv(file, sep="\t", header=None, on_bad_lines="skip")
        except pd.errors.ParserError:
            # Versuche Semikolon als Trennzeichen
            df = pd.read_csv(file, sep=";", header=None, on_bad_lines="skip")
        except pd.errors.ParserError:
            # Versuche Komma als Trennzeichen
            df = pd.read_csv(file, sep=",", header=None, on_bad_lines="skip")
        except pd.errors.ParserError:
            # Versuche Leerzeichen als Trennzeichen
            df = pd.read_csv(file, sep=" ", header=None, on_bad_lines="skip")
        except:
            # Allgemeiner Fehlerfall
            print(f"Fehler beim Laden von {file}: Unbekanntes Format")
            continue

        # Füge den DataFrame zur Liste hinzu
        dfs.append(df)
    except Exception as e:
        print(f"Fehler beim Laden von {file}: {e}")

# Überprüfe, ob Daten geladen wurden
if not dfs:
    print("Keine Daten gefunden. Überprüfe die Dateien im 'data'-Ordner.")
else:
    # Füge die DataFrames zusammen
    df_combined = pd.concat(dfs, ignore_index=True)

    # Zeige die ersten 5 Zeilen an
    print(df_combined.head())

    # Speichere den kombinierten Datensatz
    df_combined.to_csv("combined_data.csv", index=False)
    print("Daten zusammengeführt und gespeichert in combined_data.csv")

