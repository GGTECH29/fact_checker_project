from transformers import pipeline

# Modell laden
classifier = pipeline("text-classification", model="./fake_news_model")

# Beispieltext
text = "Breaking News: A new study shows that chocolate is good for your health!"

# Vorhersage machen
result = classifier(text)
print(result)
