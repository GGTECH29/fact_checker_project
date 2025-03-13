import torch
import logging
import sys

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Überprüfen, ob CUDA verfügbar ist
try:
    if torch.cuda.is_available():
        logging.info(f"CUDA verfügbar: True")
        logging.info(f"CUDA-Gerät: {torch.cuda.get_device_name(0)}")
    else:
        logging.info("CUDA verfügbar: False")
except Exception as e:
    logging.error(f"Fehler bei der Überprüfung der CUDA-Verfügbarkeit: {e}")
    sys.exit(1)
