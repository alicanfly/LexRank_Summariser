import argparse
import sys
import re
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

nltk.download('punkt', quiet=True)

def preprocess(text: str) -> str:
    """Normalize whitespace and replace smart quotes/dashes."""
    text = text.strip()
    replacements = {'“':'"', '”':'"', '‘':'"', '’':'"', '—':'-', '–':'-'}
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return re.sub(r"\s+", " ", text)
