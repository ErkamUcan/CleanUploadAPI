# test_tokenize.py
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

with open("Transcripts/denemeX.txt", "r", encoding="utf-8") as f:
    text = f.read()

sentences = sent_tokenize(text, language="turkish")

print(f"{len(sentences)} cümle bulundu.")
for i, sentence in enumerate(sentences, 1):
    print(f"{i}. {sentence}")
