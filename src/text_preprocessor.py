
import re

import spacy


# Load the English NLP model once.
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """Normalize raw text before NLP processing."""

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.lower()

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text)

    # Preserve letters, digits, spaces, and common technical symbols.
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)

    # Normalize whitespace again.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_text(text: str) -> str:
    """Clean, tokenize, remove stop words, and lemmatize text."""

    cleaned_text = clean_text(text)

    if not cleaned_text:
        return ""

    doc = nlp(cleaned_text)

    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop
        and not token.is_punct
        and not token.is_space
    ]

    return " ".join(tokens)
