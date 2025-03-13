import torch
from transformers import pipeline
import gradio as gr
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

# Vorhersagefunktion
def classify_text(text):
    try:
        result = classifier(text)
        return result[0]['label']
    except Exception as e:
        return f"Fehler bei der Vorhersage: {e}"

# Gradio-Interface
iface = gr.Interface(
    fn=classify_text,
    inputs="text",
    outputs="text",
    title="Fake News Detector",
    description="Geben Sie einen Text ein, um zu überprüfen, ob er Fake News enthält."
)

# Anwendung starten
iface.launch()
