import pandas as pd

# 1. CSV-Datei laden
df = pd.read_csv("news_sample.csv")

# 2. Unnötige Spalten entfernen
# Behalte nur die Spalten "title", "content" und "type"
df = df[["title", "content", "type"]]

# 3. Spalten umbenennen (optional)
# Ändere "type" in "is_fake" (1 für "unreliable", 0 für "reliable")
df["is_fake"] = df["type"].apply(lambda x: 1 if x == "unreliable" else 0)

# 4. Unnötige Spalten entfernen
df = df[["title", "content", "is_fake"]]

# 5. Spalten umbenennen (optional)
# Ändere "content" in "text"
df.columns = ["title", "text", "is_fake"]

# 6. Bereinigte Daten speichern
df.to_csv("clean_fake_news.csv", index=False)

print("Daten erfolgreich bereinigt und gespeichert!")
