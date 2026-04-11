import spacy
import contractions
from num2words import num2words
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score

nlp = spacy.load("en_core_web_sm")


def n2word(text: str):
    num = "".join(c for c in text if c.isdigit())
    if num:
        text = text.replace(num, num2words(int(num)))
    return text

def to_contraction(text: str):
    text = text.lower()
    return contractions.fix(text)

def drop_sw(text):
    return [t for t in text if not t.is_stop]

def drop_p(text):
    return [t for t in text if not t.is_punct]

def Stemming(text):
    return [t.lemma_ for t in text]

def pre_process(doc: str):
    doc = doc.lower()
    doc = to_contraction(doc)
    doc = n2word(doc)
    doc = nlp(doc)
    doc = drop_p(doc)
    doc = drop_sw(doc)
    doc = Stemming(doc)
    return doc

def get_ngrams(tokens: list, n: int) -> list:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def vectorize(docs: list, n_gram_size: int = 1):
    processed = [pre_process(doc) for doc in docs]

    doc_ngrams = [get_ngrams(tokens, n_gram_size) for tokens in processed]

    vocab = sorted(set(ng for ngrams in doc_ngrams for ng in ngrams))

    vectors = [
        [1 if ng in doc_ng else 0 for ng in vocab]
        for doc_ng in doc_ngrams
    ]

    return vectors, vocab


all_docs = [
    "The gold medal price is high effort",
    "Winning a gold medal needs a high jump",
    "Market for a gold medal is a trade of sweat",
    "The athlete will trade all for a gold medal",
    "The gold bars price is high today",
    "Investing in gold bars needs a high rate",
    "Market for gold bars is a trade of money",
    "The bank will trade all for gold bars",
]
y_true = [0, 0, 0, 0, 1, 1, 1, 1]


X1, vocab1 = vectorize(all_docs, n_gram_size=1)
labels1 = KMeans(n_clusters=2, random_state=42).fit_predict(X1)


X2, vocab2 = vectorize(all_docs, n_gram_size=2)
labels2 = KMeans(n_clusters=2, random_state=42).fit_predict(X2)


print("=== 1-gram ===")
for doc, y, yhat in zip(all_docs, y_true, labels1):
    print(f"{doc}  (y: {y} , yhat: {yhat})")

print("\n=== 2-gram ===")
for doc, y, yhat in zip(all_docs, y_true, labels2):
    print(f"{doc}  (y: {y} , yhat: {yhat})")

def align(y_true, y_pred):
    if accuracy_score(y_true, y_pred) < 0.5:
        return [1 - l for l in y_pred]
    return list(y_pred)

print(f"\nAccuracy 1-gram : {accuracy_score(y_true, align(y_true, labels1)):.2f}")
print(f"Accuracy 2-gram : {accuracy_score(y_true, align(y_true, labels2)):.2f}")

def tokenize(text: str) -> list:
    doc = nlp(text.lower())
    doc = drop_p(doc)
    doc = drop_sw(doc)
    return Stemming(doc)


def add_padding(tokens: list) -> list:
    return ["<s>"] + tokens + ["</s>"]


def extract_windows(tokens: list, window_size: int = 1) -> list:
    padded = add_padding(tokens)
    windows = []
    for i in range(window_size, len(padded) - window_size):
        window = padded[i - window_size : i + window_size + 1]
        windows.append(" ".join(window))
    return windows


def build_vocab(all_windows: list) -> dict:
    unique = sorted(set(w for windows in all_windows for w in windows))
    return {w: i for i, w in enumerate(unique)}


def vectorize_doc(doc_windows: list, vocab: dict) -> list:
    vector = [0] * len(vocab)
    for w in doc_windows:
        if w in vocab:
            vector[vocab[w]] = 1
    return vector


D1 = "I love cats"
D2 = "Cats are chill"
D3 = "I am late"

all_docs = [D1, D2, D3]

all_windows = [extract_windows(tokenize(doc), window_size=1) for doc in all_docs]
vocab       = build_vocab(all_windows)
vectors     = [vectorize_doc(w, vocab) for w in all_windows]


print("Vocabulaire de fenêtres :")
for w, i in vocab.items():
    print(f"  {i}: \"{w}\"")

print("\nFenêtres par document :")
for doc, windows in zip(all_docs, all_windows):
    print(f"  {doc} → {windows}")

print("\nVecteurs :")
for doc, vec in zip(all_docs, vectors):
    print(f"  {doc:<20} → {vec}")