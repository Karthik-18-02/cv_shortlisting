# install_spacy_model.py
import spacy
from spacy.cli import download

# Try to load the spaCy model
try:
    spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    download("en_core_web_sm")
