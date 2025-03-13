import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch

# 1. Bereinigte Daten laden
df = pd.read_csv("clean_fake_news.csv")

# 2. Daten in Trainings- und Testsets aufteilen
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"].tolist(), df["is_fake"].tolist(), test_size=0.2
)

# 3. Tokenisierung der Texte
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# 4. Datensätze erstellen
class FakeNewsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = FakeNewsDataset(train_encodings, train_labels)
val_dataset = FakeNewsDataset(val_encodings, val_labels)

# 5. Modell initialisieren
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# 6. Training-Argumente festlegen
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
    logging_dir="./logs",
    fp16=True,  # Nur für NVIDIA-GPUs aktivieren
)

# 7. Trainer initialisieren
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# 8. Modell trainieren
trainer.train()

# 9. Modell speichern
model.save_pretrained("./fake_news_model")
tokenizer.save_pretrained("./fake_news_model")

print("Modelltraining abgeschlossen und Modell gespeichert!")
