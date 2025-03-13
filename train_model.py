import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Daten laden
try:
    df = pd.read_csv("clean_fake_news.csv")
    logging.info("Daten erfolgreich geladen.")
except FileNotFoundError:
    logging.error("Fehler: Die Datei 'clean_fake_news.csv' wurde nicht gefunden.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    logging.error("Fehler: Die Datei 'clean_fake_news.csv' ist leer oder enthält keine gültigen Daten.")
    sys.exit(1)

# Überprüfen, ob die erforderlichen Spalten vorhanden sind
required_columns = ["title", "text", "is_fake"]
if not all(column in df.columns for column in required_columns):
    logging.error("Fehler: Die CSV-Datei enthält nicht alle erforderlichen Spalten.")
    sys.exit(1)

# Daten vorbereiten
X = df["text"]
y = df["is_fake"]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Tokenizer und Modell laden
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Datensätze tokenisieren
train_encodings = tokenizer(X_train.tolist(), truncation=True, padding=True)
val_encodings = tokenizer(X_val.tolist(), truncation=True, padding=True)

# Datensätze in PyTorch-Datensätze umwandeln
class NewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = NewsDataset(train_encodings, y_train.tolist())
val_dataset = NewsDataset(val_encodings, y_val.tolist())

# TrainingArguments und Trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Modell trainieren
try:
    trainer.train()
    logging.info("Modelltraining abgeschlossen.")
except Exception as e:
    logging.error(f"Fehler beim Modelltraining: {e}")
    sys.exit(1)

# Modell speichern
try:
    model.save_pretrained("./fake_news_model")
    logging.info("Modell erfolgreich gespeichert.")
except Exception as e:
    logging.error(f"Fehler beim Speichern des Modells: {e}")
    sys.exit(1)
