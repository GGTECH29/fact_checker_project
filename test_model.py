import torch
from transformers import pipeline
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Überprüfen, ob CUDA verfügbar ist
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Verwende Gerät: {device}")

# Modell laden
try:
    classifier = pipeline("text-classification", model="./fake_news_model", device=0 if device == "cuda" else -1)
    logging.info("Modell erfolgreich geladen.")
except Exception as e:
    logging.error(f"Fehler beim Laden des Modells: {e}")
    sys.exit(1)

# Testen
text = "The moon is made of green cheese."
try:
    result = classifier(text)
    logging.info(f"Vorhersage: {result}")
except Exception as e:
    logging.error(f"Fehler bei der Vorhersage: {e}")
    sys.exit(1)
