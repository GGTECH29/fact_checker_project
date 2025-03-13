import gradio as gr
from transformers import pipeline

# 1. Modell laden
classifier = pipeline("text-classification", model="./fake_news_model")

# 2. Funktion für die Vorhersage
def check_news(text):
    result = classifier(text)[0]
    label = "Fake News" if result["label"] == "LABEL_1" else "Echte Nachricht"
    confidence = result["score"]
    return f"{label} (Confidence: {confidence:.2f})"

# 3. Gradio-Interface erstellen
interface = gr.Interface(
    fn=check_news,  # Funktion, die aufgerufen wird
    inputs=gr.Textbox(lines=2, placeholder="Gib einen Text ein..."),  # Eingabefeld
    outputs="text",  # Ausgabefeld
    title="Fact-Checker 3000",  # Titel der UI
    examples=[
        ["Breaking News: A new study shows that chocolate is good for your health!"],
        ["The moon is made of green cheese."]
    ]
)

# 4. UI starten
interface.launch()
