
import re

def clean_text(text):
    text = text.lower() 
    symbols = ['@', '#', '$', '&', '*', '_', '-', '–']
    for s in symbols:
        text = text.replace(s, '')
    
    cleaned = ""
    for char in text:
        if char.isalpha() or char.isspace() or char == '%':
            cleaned += char
    
    cleaned = " ".join(cleaned.split())
    
    return cleaned

with open("task1.txt", "r", encoding="utf-8") as f:
    text = f.read()
cleaned_text = clean_text(text)
print(" Cleaning text :")
print(cleaned_text)

# TASK 2 :Text normalisation
from num2words import num2words
def expand_contractions(text):
    contractions = {
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
        "didn't": "did not",
        "isn't": "is not",
        "aren't": "are not",
        "they're": "they are",
        "we're": "we are",
        "that's": "that is",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "it'll": "it will"
    }
    for c in contractions:
        text = re.sub(r"\b{}\b".format(re.escape(c)), contractions[c], text)
    return text

def digits_to_words(text):
    return re.sub(r'\b\d+\b', lambda x: num2words(int(x.group())), text)

def normalize_text(text):
    text = text.lower()              
    text = expand_contractions(text)
    text = digits_to_words(text)     
    cleaned = "".join([c if c.isalnum() or c.isspace() else "" for c in text])
    cleaned = " ".join(cleaned.split())
    return cleaned

with open("task2.txt", "r", encoding="utf-8") as f:
    text = f.read()

normalized_text = normalize_text(text)
print("Normalized text :")
print(normalized_text)
